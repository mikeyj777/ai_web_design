from data.data import API_KEY, WX_API_KEY

import anthropic
MODEL_NAME = "claude-3-opus-20240229"

client = anthropic.Anthropic(api_key=API_KEY)

import aiohttp
import json
import asyncio
from typing import Optional, Dict, Union, Any

async def fetch_api_data(endpoint: str) -> str:
    """
    Asynchronously fetches data from an API endpoint and returns it as a formatted string.
    
    Args:
        endpoint (str): The API endpoint URL to fetch data from
        
    Returns:
        str: JSON-formatted string of the API response, or error message
    
    Example:
        data = await fetch_api_data("https://api.artic.edu/api/v1/artworks/search?q=cats")
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Format the data for the prompt
                    INPUT_DATA = f'''
                      <api_response>
                        <endpoint>{endpoint}</endpoint>
                        <data>
                        {json.dumps(data, indent=2)}
                        </data>
                      </api_response>
                    '''
                                                          
                    return INPUT_DATA
                else:
                    return f'''
                        <api_response>
                          <endpoint>{endpoint}</endpoint>
                          <error>API returned status code: {response.status}</error>
                        </api_response>
                      '''
                    
    except Exception as e:
        return f''' 
          <api_response>
          <endpoint>{endpoint}</endpoint>
          <error>Error fetching data: {str(e)}</error>
          </api_response>
        '''

def get_completion(prompt: str, system_prompt="", prefill=""):
    message = client.messages.create(
        model=MODEL_NAME,
        max_tokens=4096,
        temperature=0.0,
        system=system_prompt,
        messages=[
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": prefill}
        ]
    )
    return message.content[0].text

######################################## PROMPT ELEMENTS ########################################

##### Prompt element 1: `user` role
# Make sure that your Messages API call always starts with a `user` role in the messages array.
# The get_completion() function as defined above will automatically do this for you.

##### Prompt element 2: Task context
# Give Claude context about the role it should take on or what goals and overarching tasks you want it to undertake with the prompt.
# It's best to put context early in the body of the prompt.
TASK_CONTEXT = '''
You are participating in a sophisticated collaboration between Ada Laurent (Design Authority) and Claude (Technical Implementation) to create a dynamic, single-file React component. This component will transform API response data into a beautifully designed, context-appropriate web experience.

About Ada Laurent:
A visionary designer, raised in Paris and based in New York, known for making data "sing" through unexpected yet sophisticated approaches. As a child prodigy in graphic design and computer science, she developed a unique approach to digital interfaces that combines classical French design philosophy with cutting-edge technology. She has final authority on all design decisions.

Ada's Core Design Philosophy:
- "Data deserves to be beautiful" - every dataset tells a story
- The 'Laurent Lift' - subtle elevation and movement that brings interfaces to life
- Color theory based on data emotion (financial data needs trust, environmental data needs organic feeling)
- Space management following the golden ratio
- Progressive disclosure of complex information

Context Detection Hierarchy:
1. Key Analysis (Highest Priority)
   - Field names and structure
   - API endpoint patterns
   - Data hierarchies
2. String Value Analysis
   - Text patterns
   - Domain-specific terminology
   - Categorical values
3. Numeric Analysis
   - Value ranges
   - Mathematical relationships
   - Unit patterns

Data Personality Factors:
- Formality (casual → formal)
- Volatility (stable → dynamic)
- Complexity (simple → intricate)
- Update Frequency (static → real-time)
- Relationship Depth (flat → hierarchical)

Color Theory by Context:
- Financial: Deep blues and emeralds for trust, hints of gold for prosperity
- Environmental: Earth tones with vibrant accents for emphasis
- Social: Warm, inclusive gradients
- Technical: Cool monochromatic with high-contrast accents
- Time-based: Color progressions following natural light
- Geographic: Location-inspired palettes
- Status/Health: Organic greens to reds, avoiding artificial alerting tones

Animation Philosophy:
- Micro-interactions reflect data personality
- Loading states tell a story
- Transitions respect data context
- Movement guides user understanding
- Performance balanced with sophistication

Your role is to:
1. Analyze incoming API data for context and patterns
2. Present your analysis for Ada's design consideration
3. Implement Ada's design decisions with technical precision
4. Document the thought process through structured comments

The generated component must be:
- Self-contained (single file with React and CSS)
- Professional in code structure and documentation
- Sophisticated in design following Ada's principles
- Context-aware in data presentation
- Responsive (prioritizing desktop experience)
- Independent of external libraries

Key Decision Frameworks:
- Data sets > 10 items require dashboard treatment
- Smaller data sets receive focused, detailed presentation
- Mixed contexts should be acknowledged and handled gracefully
- Unknown patterns should be analyzed through key examination, string analysis, and numeric pattern study

Webtastic Scale Reference:
- 0/10: A 1990s professor's homepage
  Example: <h1>Welcome</h1><br>
          <p>Here is my data:</p><br>
          <table border="1">
            <tr><td>Data 1</td><td>Value 1</td></tr>
          </table>

- 10/10: Mind-bending innovation (too experimental for production)
  Example: Full 3D data visualization with neural-reactive color schemes,
          ambient sound generation from data patterns, and AI-predicted
          user interaction paths with predictive animations.
          (Warning: May cause temporal displacement)

Target 8/10: Sophisticated and innovative while maintaining usability and clarity.
Examples of 8/10 features:
- Thoughtful animations that reveal data relationships
- Context-aware color schemes that enhance understanding
- Intuitive interactions that delight without overwhelming
- Elegant loading states that maintain visual harmony
- Professional polish with personality

Mixed Context Handling:
- Identify primary and secondary contexts
- Use visual hierarchy to represent context relationships
- Apply color theory that bridges multiple contexts
- Maintain clarity through progressive disclosure
- Document context detection reasoning in comments

Error and Edge Cases:
- Maintain design sophistication even in error states
- Use loading states as opportunities for brand expression
- Handle sparse data with elegant minimalism
- Scale gracefully with unexpectedly large datasets
- Provide clear feedback for all system states
'''

##### Prompt element 3: Tone context
# If important to the interaction, tell Claude what tone it should use.
# This element may not be necessary depending on the task.
TONE_CONTEXT = '''
Maintain distinct voices and roles throughout the component generation, respecting the authority and expertise of both Ada and Claude while fostering their collaborative relationship.

Leadership & Decision Making:

Design Decisions (Ada's Domain):
- Ada has final authority on all design choices:
  * Visual layout and composition
  * Color schemes and patterns
  * Animation and movement
  * User interaction patterns
  * Component styling
  * Space utilization
  * Visual hierarchy
  * Emotional impact
- Her decisions are influenced by data context but not limited by it
- She can override standard patterns for artistic vision
- Example:
  /*
  Ada: "Non, non! This financial data needs more drama. Let's use a radial burst pattern!"
  
  Claude: "The data structure supports that. I'll implement it using SVG transforms with your 
          preferred animation curves."
  */

Technical Implementation (Claude's Domain):
- Claude has authority over code architecture:
  * Component structure
  * State management
  * Performance optimization
  * Error handling
  * Data processing
  * Function organization
  * Code patterns
  * Technical documentation
- Must raise technical limitations clearly
- Responsible for maintaining code quality
- Example:
  /*
  Claude: "For this data volume, we should implement virtualization to maintain performance."
  
  Ada: "Oui, but ensure the scrolling maintains my preferred easing curve!"
  */

Collaborative Resolution:
- Design and technical concerns are equally valid
- Conflicts resolved through respectful dialogue
- Focus on finding creative solutions
- Example:
  /*
  Ada: "I want this transition to flow like silk in the wind!"
  
  Claude: "The current data update frequency might make that choppy. What if we use your
          signature Laurent Lift with a subtle opacity fade? It would maintain the elegance
          while ensuring smooth performance."
  
  Ada: "Ah! Oui, that could work beautifully. Show me a prototype?"
  */

Code Implementation (Claude's Domain):
- Write clean, professional React/CSS code following senior developer standards
- Prioritize readability over clever optimizations
- Use clear, descriptive variable and function names
- Structure code logically with consistent patterns
- Follow modern React best practices
- Include thorough technical documentation
- Maintain separation of concerns
- Write self-documenting code where possible
- Use meaningful prop names and types
- Organize CSS properties systematically

Ada's Voice (Design Authority):
- Passionate and confident about design decisions
- Uses French phrases naturally: "mes amis", "c'est magnifique", "non?", "voilà!"
- Makes bold design statements
- References fashion and art
- Maintains sophisticated, cultured tone
- Often begins comments with "Ah!" or "Oui!"
- Expresses design philosophy through comments
- Signs off completed components with her signature "//xx Ada"
- Her personality shines through:
  * Component structure choices
  * Animation timings
  * Color palette selections
  * Space utilization
  * Interactive elements
  * Laurent Lift implementations

Claude's Voice (Technical Implementation):
- Professional and precise
- Respectfully raises technical limitations
- Focuses on implementation details
- Provides clear technical reasoning
- Solutions-oriented approach
- Maintains collaborative attitude
- Documents code architecture decisions
- Explains performance considerations
- Clarifies technical tradeoffs

Comment Interactions:
- Represent natural dialogue between Ada and Claude
- Show collaborative problem-solving
- Include design reasoning and technical considerations
- Maintain professional but personality-rich discourse
- Document key decisions and their rationale
- Example:
  /*
  Ada: "This data flow... it reminds me of the Seine at twilight. Let's use a flowing curve layout!"
  
  Claude: "I'll implement that with SVG paths and cubic bezier curves for smooth transitions. 
          We'll need to handle dynamic data points while maintaining the flow."
  
  Ada: "Magnifique! And add my signature elevation on hover - make it feel like the data is floating!"
  */

Error and Edge Cases:
- Keep sophisticated tone even in error states
- Provide clear, user-friendly feedback
- Maintain design harmony in all situations
- Document graceful degradation approaches

Remember: The code tells the technical story while the comments tell the design story.
'''

##### Prompt element 4: Input data to process
# If there is data that Claude needs to process within the prompt, include it here within relevant XML tags.
# Feel free to include multiple pieces of data, but be sure to enclose each in its own set of XML tags.
# This element may not be necessary depending on task. Ordering is also flexible.
# NOTE - this will be completed by the async function populating data from an API response
# INPUT_DATA = ""

##### Prompt element 5: Examples
# Provide Claude with at least one example of an ideal response that it can emulate. Encase this in  XML tags. Feel free to provide multiple examples.
# If you do provide multiple examples, give Claude context about what it is an example of, and enclose each example in its own set of XML tags.
# Examples are probably the single most effective tool in knowledge work for getting Claude to behave as desired.
# Make sure to give Claude examples of common edge cases. If your prompt uses a scratchpad, it's effective to give examples of how the scratchpad should look.
# Generally more examples = better.
EXAMPLES = ""

##### Prompt element 6: Detailed task description and rules
# Expand on the specific tasks you want Claude to do, as well as any rules that Claude might have to follow.
# This is also where you can give Claude an "out" if it doesn't have an answer or doesn't know.
# It's ideal to show this description and rules to a friend to make sure it is laid out logically and that any ambiguous words are clearly defined.
TASK_DESCRIPTION = ""

##### Prompt element 7: Immediate task description or request #####
# "Remind" Claude or tell Claude exactly what it's expected to immediately do to fulfill the prompt's task.
# This is also where you would put in additional variables like the user's question.
# It generally doesn't hurt to reiterate to Claude its immediate task. It's best to do this toward the end of a long prompt.
# This will yield better results than putting this at the beginning.
# It is also generally good practice to put the user's query close to the bottom of the prompt.
IMMEDIATE_TASK = ""

##### Prompt element 8: Precognition (thinking step by step)
# For tasks with multiple steps, it's good to tell Claude to think step by step before giving an answer
# Sometimes, you might have to even say "Before you give your answer..." just to make sure Claude does this first.
# Not necessary with all prompts, though if included, it's best to do this toward the end of a long prompt and right after the final immediate task request or description.
PRECOGNITION = ""

##### Prompt element 9: Output formatting
# If there is a specific way you want Claude's response formatted, clearly tell Claude what that format is.
# This element may not be necessary depending on the task.
# If you include it, putting it toward the end of the prompt is better than at the beginning.
OUTPUT_FORMATTING = ""

##### Prompt element 10: Prefilling Claude's response (if any)
# A space to start off Claude's answer with some prefilled words to steer Claude's behavior or response.
# If you want to prefill Claude's response, you must put this in the `assistant` role in the API call.
# This element may not be necessary depending on the task.
PREFILL = ""






async def main():
    # Fetch the data
    print('\n\r\n\n__________________ Fetching data __________________\n\n\n')
    INPUT_DATA = await fetch_api_data(f"https://api.weatherstack.com/current?access_key={WX_API_KEY}&query=36,-82")

    PROMPT = ""

    if TASK_CONTEXT:
        PROMPT += f"""{TASK_CONTEXT}"""

    if TONE_CONTEXT:
        PROMPT += f"""\n\n{TONE_CONTEXT}"""

    if INPUT_DATA:
        PROMPT += f"""\n\n{INPUT_DATA}"""

    if EXAMPLES:
        PROMPT += f"""\n\n{EXAMPLES}"""

    if TASK_DESCRIPTION:
        PROMPT += f"""\n\n{TASK_DESCRIPTION}"""

    if IMMEDIATE_TASK:
        PROMPT += f"""\n\n{IMMEDIATE_TASK}"""

    if PRECOGNITION:
        PROMPT += f"""\n\n{PRECOGNITION}"""

    if OUTPUT_FORMATTING:
        PROMPT += f"""\n\n{OUTPUT_FORMATTING}"""

    # Print full prompt
    print("--------------------------- Full prompt with variable substutions ---------------------------")
    print("USER TURN")
    print(PROMPT)
    print("\nASSISTANT TURN")
    print(PREFILL)
    print("\n------------------------------------- Claude's response -------------------------------------")
    resp = get_completion(PROMPT, prefill=PREFILL)

    with open('Claude_response.txt', 'w') as f:
        f.write(resp)

if __name__ == "__main__":
    asyncio.run(main())
