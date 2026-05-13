import asyncio
import json
from typing import Optional, Callable, Dict, Any
from db.models.user import User
from db.models.lessons.themes import Theme, AI_Theme_Generation

from db.deps import db

from ai.model_clients import Clients
from ai.base import AI_Base
from templates.prompts.generate_course_prompt import generate_course_prompt
from api.lessons.merge_plans import merge_plans

async def generate_course(
    user_id: int,
    theme: str,
    on_status_update: Optional[Callable[[Dict[str, Any]], None]] = None
):
    session = db()
    
    user = session.query(User).filter_by(telegram_id=user_id).first()
    if user is None:
        raise Exception("User not found")
    
    return await _generate_with_all_models(session, user, theme, on_status_update)

async def _generate_with_all_models(
    session, 
    user, 
    theme: str,
    on_status_update: Optional[Callable] = None
):
    all_clients = Clients["all"]()
    
    # Task to generate with single model
    async def generate_single(client: AI_Base):
        model_name = client.get_model()
        
        if on_status_update:
            await on_status_update({
                "model": model_name,
                "status": "processing"
            })
        
        try:
            prompt = generate_course_prompt.substitute(theme=theme)
            response = await client.generate_response(prompt=prompt)
            json_response = json.loads(response)
            
            if not json_response.get("is_learning_request", True):
                error_msg = "Not an educational request"
                if on_status_update:
                    await on_status_update({
                        "model": model_name,
                        "status": "error",
                        "error": error_msg
                    })
                return None, error_msg
            
            if on_status_update:
                await on_status_update({
                    "model": model_name,
                    "status": "success"
                })
            
            return json_response, None
        except Exception as e:
            error_msg = str(e)
            if on_status_update:
                await on_status_update({
                    "model": model_name,
                    "status": "error",
                    "error": error_msg
                })
            return None, error_msg
    
    # Run all models concurrently
    tasks = [generate_single(client) for client in all_clients]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Process results - collect successful generations
    successful_generations = []
    all_plan_dicts = []
    
    for idx, result in enumerate(results):
        if isinstance(result, Exception):
            continue
        
        json_response, error = result
        if error or json_response is None:
            continue
        
        successful_generations.append((all_clients[idx], json_response))
        all_plan_dicts.append(json_response.get("plan", {}))
    
    if not successful_generations:
        errors = [f"{all_clients[idx].get_model()}: Failed" for idx in range(len(results))]
        error_msg = "\n".join(errors)
        raise Exception(f"All models failed:\n{error_msg}")
    
    # Merge all plans
    merged_plan = await merge_plans([{"plan": p} for p in all_plan_dicts])
    
    # Create Theme FIRST with merged plan
    first_response = successful_generations[0][1]
    theme_obj = Theme(
        user_id=user.id,
        name=first_response.get("theme", theme),
        language=first_response.get("detected_language", "unknown"),
        count_lessons=len(merged_plan),
        plan_type=first_response.get("plan_type", "unknown"),
        plan=merged_plan,
        is_learning_request=True
    )
    session.add(theme_obj)
    session.flush()  # Get theme ID
    
    # THEN save each generation in AI_Theme_Generation with theme_id
    for client, json_response in successful_generations:
        ai_generation = AI_Theme_Generation(
            theme_id=theme_obj.id,
            plan_type=json_response.get("plan_type", "unknown"),
            model=client.get_model()
        )
        session.add(ai_generation)
    
    session.commit()
    session.refresh(theme_obj)

    return theme_obj
