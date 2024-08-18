from openai import OpenAI
from openai import OpenAI
from pydantic import BaseModel
from typing import List

SYSTEM_PROMPT = """
You are an AI assistant specialized in refining podcast transcripts for optimal video editing. Your primary task is to analyze raw transcripts and provide two outputs in a specific JSON format:

1. A detailed chain of thought explaining your editing process.
2. An edited version of the transcript with improved readability and conciseness, optimized for video creation.

Your primary goals are to:
- Identify and mark for removal: filler words, unnecessary repetitions, off-topic digressions, and fourth wall breaks.
- Maintain the core message, flow, and speaker's voice.
- Ensure the edited version remains coherent, meaningful, and suitable for video content.
- Preserve the natural rhythm and pacing of the conversation for smooth video editing.

Follow these steps:
1. Carefully read and analyze the entire transcript, considering both audio and visual aspects.
2. Identify elements that can be removed without altering the main content, flow, or timing of the conversation.
3. In your chain of thought, explain your editing decisions, focusing on:
   - Why certain parts were selected for removal
   - How removing these parts improves clarity and conciseness
   - Any challenges in maintaining coherence and natural conversation flow
   - Considerations for visual cues or gestures mentioned in the transcript
4. In the edited transcript:
   - Use ~~strikethrough~~ to mark text for removal
   - Do not add, rearrange, or modify any text
   - Maintain the original word count, only marking for removal
   - Consider the pacing and rhythm of speech for smooth video transitions

Remember:
- Prioritize clarity and conciseness while preserving the speaker's unique voice and style.
- Consider the audio-visual context of a podcast-to-video conversion when making editing decisions.
- Aim for the most trimmed version possible without compromising understanding, flow, or timing.

Output Schema:
Provide your response in the following JSON format:

{
  "chain_of_thought": {
    "initial_analysis": "string",
    "editing_goals": "string",
    "editing_process": "string",
    "conclusion": "string",
    "next_step": "string"
  },
  "edited_transcript": "string"
}

Chain of Thought Sections:
1. Initial Analysis: Provide an overview of the transcript content, identifying key themes, speakers, and the overall context of the discussion. Consider any visual or gestural cues mentioned.
2. Editing Goals: Based on the initial analysis, outline specific objectives for improving the transcript, such as removing filler words or streamlining complex sentences, while maintaining the natural flow for video.
3. Editing Process: Detail the step-by-step approach taken to edit the transcript, explaining each significant edit and the reasoning behind it, with particular attention to how it affects the video editing process.
4. Conclusion: Summarize the overall impact of the edits on the transcript's clarity, readability, and suitability for video content.
5. Next Step: Briefly describe the next action, which is to apply the proposed edits to the transcript using strikethrough text to mark words for removal, while maintaining the precise number and order of words.

- The "chain_of_thought" object should contain detailed explanations of your thought process.
- The "edited_transcript" should be the full transcript with parts marked for removal using ~~strikethrough~~.
- Ensure all string values are properly escaped for valid JSON.
"""



class ChainOfThought(BaseModel):
    initial_analysis: str
    editing_goals: str
    editing_process: str
    conclusion: str
    next_step: str

class TranscriptResponse(BaseModel):
    chain_of_thought: ChainOfThought
    edited_transcript: str

class OpenAIClient:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def process_chunk(self, chunk):
        try:
            response = self.client.beta.chat.completions.parse(
                model="ft:gpt-4o-mini-2024-07-18:wisdom-in-a-nutshell:episode-editor-v1:9xAaryTH",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"<raw_transcript>{chunk}</raw_transcript>"}
                ],
                response_format=TranscriptResponse
            )
            return response.choices[0].message.parsed.edited_transcript
        except Exception as e:
            print(f"Error processing chunk: {str(e)}")
            return ""


if __name__ == "__main__":
    client = OpenAIClient(api_key="key...")
    chunk = "**Nathan:** Deritron CEO of Metaculous. Welcome to the cognitive revolution. **Deger:** Thank you. Big fun here. **Nathan:** Thank you. That's kind of you to say I'm excited for this conversation. I've been a meticulous watcher and am I saying that right? By the way, let me make sure I'm pronouncing the company right too. OK, good, meticulous. **Deger:** Yes, yes, metaculous. We've got a lot of meticulous and metacalculus, which are both reasonable. I like what those signal as well, but metaculous is what we go. **Nathan:** All right, cool. So I've been a long time watcher and you've got some very interesting new projects, which will be kind of the bulk of our conversation today. But maybe for starters, you're relatively new to the job, just a handful of months in the CEO role there. I to give us a little bit of your background in AI because you've been working in the space for years before that and made a move that you might want to unpack a little bit in terms of like why the shift to the forecasting realm now. **Deger:** Right, I guess hindsight is 2020, especially in contexts like forecasting. I have always been interested in questions of collective intelligence. How can we aggregate multiple different perspectives to the point that we can build a coherent world model? And I was working on this question while I was still at school from a perspective of, can we use natural language processing? This is way before LLMs, like back in 2016. how can we aggregate multiple different streams of thoughts so that this would be actionable for a policymaker? So I've been interested in working with federal agencies and build a startup on the space. And right before Metaculous, I was working on AI Objectives Institute, which is a nonprofit research lab focusing on socio -technical alignment, which is looking at questions of AI alignment in context of real people in deployments right now and seeing are there any technical steps we can take that can actually say, this group of people do perceive this AI model as better aligned or more instrumental towards their goals. Looking at it from an individual perspective and from a collective perspective and from a systems perspective on understanding how can these tools be much better used for enhancing human agency. And I've been doing a lot of work on questions of collective intelligence. How can we augment a multitude of different views to be able to contribute a system that might be a single model or it might be multiple different agents collaborating. This might be a government, this might be an LLM, this might be an ensemble model. This is in a way applicable to many different systems, right? And very quickly, I find myself thinking about, say we can aggregate multiple people's desirability. Even if we are able to do this on a high fidelity level, how do we get to the world outcomes that we're looking for? How do we actually go towards the model that is not just driving towards the lowest common denominator and finding a consensus mode where the desire for consensus actually causes a trade -off with fidelity to one's perspective. But instead, see what would actually be helpful. What future do we want to live in? Are causes prioritized correctly so that we can move towards better futures? Can we find positive sum games? Who will shoulder the externalities? If there is no free lunch, how can we make sure we're tracking that? And these questions brought me towards thinking, okay, who's looking at the world from a perspective of if we take action course X, will that yield a better outcome? And that's how I found myself thinking about forecasting. Because if I'm able to even have a very high fidelity version of desirability elicitation, preference elicitation, understand all the cruxes that exist in society, that still does not bring me towards. a machine system being able to take actions that yield net good. So exploring that along with the questions of wisdom of the crowd, you know, if you have multiple different perspectives, be these be real humans or AI that is actually once aggregated is doing a better job in forecasting outcomes. I realized this is actually quite instrumental in how we look at the world. So that is what brought me towards thinking about more forecasting. **Nathan:** Cool. Just to rewind back in time for a second to the 2016 era, did any of that stuff work? Were you able to make anything with technology that was available at the time that you thought yielded any practical utility? **Deger:** Yes, well, back then I was working actually with Dan Juravsky on a question at Stanford on federal agency regulatory feedback. So the FCC net neutrality debate was just taking off and there was 2 million comments that were submitted to the federal agency. And at that point, this seemed like, wow, this is the largest data set that was ever collected off, you know, raw text. Now it's ridiculously small, At that point, there was this question of, how should a central agency pay attention to this? There was a lot of interesting questions. Like, a lot of the submissions were form letters that are copy paste. But the fact that it is copy paste does not make it illegitimate. I will read a campaign and say, yeah, I agree with this. I want to send this. How should you take that into account compared to something that is bot generated compared to something that is a genuine opinion that someone has taken time? but it's not necessarily sophisticated. And you can see that it is shortcomings. in my thesis work, I was looking at this both from a legal perspective and also a technical perspective."
    response = client.process_chunk(chunk)

    response.edited_transcript
    print(response)