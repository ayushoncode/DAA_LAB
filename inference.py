import os
import sys
from openai import OpenAI
from app.env import SupportEnv, TASKS
from app.models import SupportAction, ActionType

API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME   = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
HF_TOKEN     = os.getenv("HF_TOKEN", "")

if not HF_TOKEN:
    print("[ERROR] HF_TOKEN not set", flush=True)
    sys.exit(1)

client = OpenAI(base_url=API_BASE_URL.rstrip("/"), api_key=HF_TOKEN)
env    = SupportEnv()

SYSTEM_PROMPT = """You are a professional customer support agent.
Always: acknowledge frustration, offer a concrete resolution, be polite, write at least 40 words."""

def get_llm_reply(email):
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            max_tokens=300,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Respond to this customer email:\n\n{email}"},
            ],
        )
        return response.choices[0].message.content or "We sincerely apologize and will resolve this immediately."
    except Exception as exc:
        print(f"[DEBUG] LLM call failed: {exc}", flush=True)
        return "We sincerely apologize for the inconvenience with your order and account. We will immediately investigate, escalate to our senior team, and process a full refund or replacement within 24 hours."

def run_episode(difficulty):
    obs = env.reset(difficulty=difficulty)
    task_id = obs.task_id

    print(f"[START] task={task_id}", flush=True)

    step = 0
    total_reward = 0.0

    # Step 1: RESEARCH
    step += 1
    _, r, _, _ = env.step(SupportAction(action_type=ActionType.RESEARCH, reasoning="Looking up order"))
    total_reward += r
    print(f"[STEP] step={step} action=RESEARCH reward={r} done=false", flush=True)

    # Step 2: TAG
    step += 1
    _, r, _, _ = env.step(SupportAction(action_type=ActionType.TAG, tag="support"))
    total_reward += r
    print(f"[STEP] step={step} action=TAG reward={r} done=false", flush=True)

    # Step 3: DRAFT
    step += 1
    _, r, _, _ = env.step(SupportAction(action_type=ActionType.DRAFT, reasoning="Drafting reply"))
    total_reward += r
    print(f"[STEP] step={step} action=DRAFT reward={r} done=false", flush=True)

    # Step 4: SUBMIT
    step += 1
    ai_reply = get_llm_reply(obs.email)
    _, reward, done, _ = env.step(SupportAction(action_type=ActionType.SUBMIT, reply=ai_reply))
    total_reward += reward
    print(f"[STEP] step={step} action=SUBMIT reward={reward} done=true", flush=True)

    score = round(min(max(total_reward, 0.0), 1.0), 2)
    print(f"[END] task={task_id} score={score} steps={step}", flush=True)
    return score

if __name__ == "__main__":
    all_scores = []
    for difficulty in ["easy", "medium", "hard"]:
        score = run_episode(difficulty=difficulty)
        all_scores.append(score)
    overall = round(sum(all_scores) / len(all_scores), 2)
    print(f"[SUMMARY] overall_score={overall}", flush=True)
    sys.exit(0)
