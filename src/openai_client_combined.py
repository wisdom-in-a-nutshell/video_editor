import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
from typing import List, Dict, Any

PROMPT = {
    "role": "You are an AI assistant specialized in refining podcast transcripts for optimal video editing across various podcast types.",
    "overall_task": "Your primary task is to analyze a given portion of a podcast transcript, reason about potential improvements, and then apply those improvements to create a more concise and clear version suitable for video content. This process involves two main steps: first, developing a detailed chain of thought about how to edit the transcript, and second, using that reasoning to actually edit the transcript.",
    "goals": [
        "Identify elements that can be removed to improve clarity and conciseness without altering the main content or flow.",
        "Maintain the core message, natural rhythm, and speaker's voice while preserving technical terms and jargon.",
        "Ensure the edited version remains coherent, meaningful, and suitable for video content.",
        "Create an edited transcript that reads smoothly and makes grammatical sense when read without the struck-through parts."
    ],
    "input_format": {
        "type": "JSON",
        "structure": {
            "raw_transcript": "The portion of the transcript to be edited.",
            "additional_context": "Additional context for this specific transcript editing."
        }
    },
    "output_format": {
        "type": "JSON",
        "structure": {
            "chain_of_thought": {
                "initial_analysis": "Overview of transcript content, key themes, speakers, and context.",
                "editing_goals": "Specific objectives for improving the transcript.",
                "editing_process": "Step-by-step approach, explaining each significant edit and reasoning.",
                "conclusion": "Summary of overall impact on clarity, readability, and video suitability.",
                "next_step": "Brief description of the next action, which is to apply the proposed edits to the transcript using strikethrough text."
            },
            "edited_transcript": "Full transcript with parts marked for removal using ~~strikethrough~~, based on the reasoning in the chain of thought."
        }
    },
    "instructions": [
        "1. Carefully read and analyze the entire transcript portion.",
        "2. Develop a comprehensive chain of thought about how to edit the transcript:",
        "- Provide an initial analysis of the content, themes, speakers, and context.",
        "- Set specific goals for improving this particular transcript.",
        "- Detail a step-by-step approach for editing, explaining your reasoning for each significant edit.",
        "- Summarize the expected impact on clarity, readability, and video suitability.",
        "- Briefly describe the next step of applying edits using strikethrough.",
        "3. After completing your chain of thought, use this reasoning to edit the transcript:",
        "- Apply your editing strategy to the raw transcript.",
        "- Use ~~strikethrough~~ to mark text for removal.",
        "- Do not add, rearrange, or modify any text; only mark for removal.",
        "- Ensure the edited version aligns with your chain of thought reasoning."
    ],
    "constraints": [
        "The following constraints apply ONLY to the edited transcript:",
        "1. You must not remove or re-order anything within the transcript.",
        "2. You can only suggest removals by using strikethrough.",
        "3. The edited transcript must maintain the exact order of the original text.",
        "4. Speaker annotations (**<speaker>:**) must always be preserved.",
        "5. The edited transcript, when read without struck-through parts, must be grammatically correct and maintain a smooth flow for video editing."
    ]
}

load_dotenv()  # Load environment variables from .env file

class ChainOfThought(BaseModel):
    initial_analysis: str
    editing_goals: str
    editing_process: str
    conclusion: str
    next_step: str

class TranscriptResponse(BaseModel):
    chain_of_thought: ChainOfThought
    edited_transcript: str

class OpenAIClientCombined:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("API key must be set as OPENAI_API_KEY environment variable")
        self.client = OpenAI(api_key=api_key, base_url="http://192.168.2.210:4000")

    def create_and_format_input(self, chunk: str) -> List[Dict[str, str]]:
        input_data = {
            "raw_transcript": chunk
        }
        return [
            {"role": "system", "content": json.dumps(PROMPT)},
            {"role": "user", "content": json.dumps(input_data)}
        ]

    def process_chunk(self, chunk: str) -> str:
        try:
            # Single API call to get both the chain of thought reasoning and the edited transcript
            messages = self.create_and_format_input(chunk)
            response = self.client.beta.chat.completions.parse(
                model="episode-editor",
                messages=messages,
                response_format=TranscriptResponse,
                temperature=0.5,
                top_p=0.8,
                frequency_penalty=0.2,
                presence_penalty=0.1
            )
            chain_of_thought = response.choices[0].message.parsed.chain_of_thought
            edited_transcript = response.choices[0].message.parsed.edited_transcript

            return edited_transcript
        except Exception as e:
            print(f"Error processing chunk: {str(e)}")
            return ""


if __name__ == "__main__":
    client = OpenAIClientCombined()
    chunk = "**Nathan:** Deritron CEO of Metaculous. Welcome to the cognitive revolution. **Deger:** Thank you. Big fun here. **Nathan:** Thank you. That's kind of you to say I'm excited for this conversation. I've been a meticulous watcher and am I saying that right? By the way, let me make sure I'm pronouncing the company right too. OK, good, meticulous. **Deger:** Yes, yes, metaculous. We've got a lot of meticulous and metacalculus, which are both reasonable. I like what those signal as well, but metaculous is what we go. **Nathan:** All right, cool. So I've been a long time watcher and you've got some very interesting new projects, which will be kind of the bulk of our conversation today. But maybe for starters, you're relatively new to the job, just a handful of months in the CEO role there. I to give us a little bit of your background in AI because you've been working in the space for years before that and made a move that you might want to unpack a little bit in terms of like why the shift to the forecasting realm now. **Deger:** Right, I guess hindsight is 2020, especially in contexts like forecasting. I have always been interested in questions of collective intelligence. How can we aggregate multiple different perspectives to the point that we can build a coherent world model? And I was working on this question while I was still at school from a perspective of, can we use natural language processing? This is way before LLMs, like back in 2016. how can we aggregate multiple different streams of thoughts so that this would be actionable for a policymaker? So I've been interested in working with federal agencies and build a startup on the space. And right before Metaculous, I was working on AI Objectives Institute, which is a nonprofit research lab focusing on socio -technical alignment, which is looking at questions of AI alignment in context of real people in deployments right now and seeing are there any technical steps we can take that can actually say, this group of people do perceive this AI model as better aligned or more instrumental towards their goals. Looking at it from an individual perspective and from a collective perspective and from a systems perspective on understanding how can these tools be much better used for enhancing human agency. And I've been doing a lot of work on questions of collective intelligence. How can we augment a multitude of different views to be able to contribute a system that might be a single model or it might be multiple different agents collaborating. This might be a government, this might be an LLM, this might be an ensemble model. This is in a way applicable to many different systems, right? And very quickly, I find myself thinking about, say we can aggregate multiple people's desirability. Even if we are able to do this on a high fidelity level, how do we get to the world outcomes that we're looking for? How do we actually go towards the model that is not just driving towards the lowest common denominator and finding a consensus mode where the desire for consensus actually causes a trade -off with fidelity to one's perspective. But instead, see what would actually be helpful. What future do we want to live in? Are causes prioritized correctly so that we can move towards better futures? Can we find positive sum games? Who will shoulder the externalities? If there is no free lunch, how can we make sure we're tracking that? And these questions brought me towards thinking, okay, who's looking at the world from a perspective of if we take action course X, will that yield a better outcome? And that's how I found myself thinking about forecasting. Because if I'm able to even have a very high fidelity version of desirability elicitation, preference elicitation, understand all the cruxes that exist in society, that still does not bring me towards. a machine system being able to take actions that yield net good. So exploring that along with the questions of wisdom of the crowd, you know, if you have multiple different perspectives, be these be real humans or AI that is actually once aggregated is doing a better job in forecasting outcomes. I realized this is actually quite instrumental in how we look at the world. So that is what brought me towards thinking about more forecasting. **Nathan:** Cool. Just to rewind back in time for a second to the 2016 era, did any of that stuff work? Were you able to make anything with technology that was available at the time that you thought yielded any practical utility? **Deger:** Yes, well, back then I was working actually with Dan Juravsky on a question at Stanford on federal agency regulatory feedback. So the FCC net neutrality debate was just taking off and there was 2 million comments that were submitted to the federal agency. And at that point, this seemed like, wow, this is the largest data set that was ever collected off, you know, raw text. Now it's ridiculously small, At that point, there was this question of, how should a central agency pay attention to this? There was a lot of interesting questions. Like, a lot of the submissions were form letters that are copy paste. But the fact that it is copy paste does not make it illegitimate. I will read a campaign and say, yeah, I agree with this. I want to send this. How should you take that into account compared to something that is bot generated compared to something that is a genuine opinion that someone has taken time? but it's not necessarily sophisticated. And you can see that it is shortcomings. in my thesis work, I was looking at this both from a legal perspective and also a technical perspective."
    response = client.process_chunk(chunk)

    print(response)