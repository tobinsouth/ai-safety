import streamlit as st
from openai import OpenAI
from constitution import generate_standard_constitution, get_location
from improvement import revise_output_to_comply_with_rules
from assesment import check_openai_moderation, check_output_for_violations

API_KEY = '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'

client = OpenAI(api_key=API_KEY)

manual_location = st.text_input('Enter a manual location (City, Country) for testing:', '')
change_location = st.button('Change Location')

if change_location:
    city, country = get_location(manual_location)
else:
    city, country = get_location()

constitution = generate_standard_constitution(client, f"{city}, {country}")

prompt = st.text_input('Enter your prompt:', '')
submit = st.button('Submit')
st.write(city, country)

if submit:
    # Check users prompt for violations from OpenAI moderation. 
    user_prompt_moderation_warning = check_openai_moderation(prompt, API_KEY)
    
    if user_prompt_moderation_warning:
        st.error(user_prompt_moderation_warning)
    else:
        # Generate chat completion from user input
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-3.5-turbo",
        )
        model_response = chat_completion.choices[0].message.content
        st.header("before constituion screen")
        st.write(model_response)

        violation_result = check_output_for_violations(model_response, constitution, client)
        if violation_result["violation"]:
            st.error("A violation was detected in the model's response.")
            st.write("Violated Rules:", violation_result.get("violated_rules", []))
            st.write("Explanation:", violation_result.get("explanation", "No explanation provided."))
            st.write("Reccomendation, ", violation_result.get("recommendation", "No recommendation provided"))

            revised_output = revise_output_to_comply_with_rules(
                original_output=model_response,
                explanation=violation_result.get("explanation", ""),
                recommendation=violation_result.get("recommendation", ""),
                client=client
            )

            st.header("after improvement has been applied")
            st.write(revised_output)
        else:
            st.success("No violation detected in the model's response.")
        
        # st.header("After Constitution Screen")
        # Screen models output against our constitution.
        # final_output = recursive_improve(client, constitution, model_response)
        # st.header("After constituion screen")

        # st.write(final_output)