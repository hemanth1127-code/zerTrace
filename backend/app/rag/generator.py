import os
import re
from app.config import settings

def generate_answer(question, context, allowed_ids):
    if not settings.GOOGLE_API_KEY:
        raise RuntimeError("GOOGLE_API_KEY not configured. Set it in .env to enable generation.")
    import google.generativeai as genai
    genai.configure(api_key=settings.GOOGLE_API_KEY)
    model = genai.GenerativeModel(settings.GEMMA_MODEL)
    
    # Build a mapping from chunk_id to short citation number
    chunk_to_num = {cid: str(i+1) for i, cid in enumerate(allowed_ids)}
    
    # Replace chunk_ids in context with short numbers
    numbered_context = context
    for cid, num in chunk_to_num.items():
        numbered_context = numbered_context.replace(f"[{cid}]", f"[{num}]")
    
    prompt = f"""Your response MUST start with "1." and contain ONLY numbered steps. Do NOT output any analysis, reasoning, goals, constraints, bullet points, or formatting markers.

Give clear numbered steps with brief practical details. Cite sources inline like [1], [2], etc.

CONTEXT:
{numbered_context}

QUESTION: {question}

1."""
    resp = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            max_output_tokens=300,
            temperature=0.1,
            top_p=0.8,
            top_k=20,
        )
    )
    
    # Post-process to extract only the actual answer (after Context:)
    text = resp.text.strip()
    
    # Split by "Context:" and take the last part (the actual answer)
    parts = text.split('Context:')
    if len(parts) > 1:
        text = parts[-1]
    
    # Also split by "Question:" and take the last part
    parts = text.split('Question:')
    if len(parts) > 1:
        text = parts[-1]
    
    # Now extract numbered steps (both "1." and "Step 1:" formats) with citations
    lines = text.split('\n')
    step_lines = []
    
    for line in lines:
        stripped = line.strip()
        # Remove leading "*   " or similar bullet prefixes
        stripped = re.sub(r'^[\*\-\•\s]+', '', stripped)
        
        # Match both "1. text [cite]" and "Step 1: text [cite]" formats
        if (re.match(r'^\s*\d+[.)]\s+\w', stripped) or re.match(r'^\s*Step\s+\d+[:.)]\s+\w', stripped)) and re.search(r'\[\d+\]', stripped):
            step_lines.append(stripped)
        elif step_lines and stripped and not re.match(r'^\s*[\*\-\•]', stripped) and not re.match(r'^\s*(Constraint|Goal|Question|Context|Step\s*\d+:)', stripped):
            # Continuation of a step
            step_lines.append(stripped)
    
    if step_lines:
        return '\n'.join(step_lines[:8])
    
    # Fallback: find all numbered patterns with citations
    all_steps = re.findall(r'(?:^|\n)\s*(\d+[.)]\s*[^\n]*\[\d+\][^\n]*)', text)
    if all_steps:
        return '\n'.join(all_steps[-8:])
    
    # Also try Step format
    all_steps = re.findall(r'(?:^|\n)\s*(Step\s+\d+[:.)]\s*[^\n]*\[\d+\][^\n]*)', text)
    if all_steps:
        return '\n'.join(all_steps[-8:])
    
    return text
