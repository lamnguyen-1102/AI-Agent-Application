import streamlit as st
from profiles import create_profile, get_notes, get_profile
from form_submit import update_personal_info, add_note, delete_note
from ai import ask_ai, get_macros, save_chat_history, load_chat_history, chat_with_ai

st.image("thumbnail.jpg")
st.title('AI-Powered Fitness Advisor')
st.write("Level up your fitness journey with personalized workouts, nutrition tips, and real-time coaching—all powered by AI. Whether you're a beginner or a pro, your AI fitness advisor adapts to your goals and keeps you motivated every step of the way.")

USER_AVATAR = "👦"
BOT_AVATAR = "🤖"

@st.fragment()
def personal_data_form():
    with st.form("personal_data"):
        st.header("📌 Personal Data")

        profile = st.session_state.profile

        name = st.text_input("Name", value = profile["general"]["name"])
        age = st.number_input("Age", min_value=1, max_value=120, step = 1, value = profile["general"]["age"])
        weight = st.number_input(
            "Weight (kg)", min_value=0.0, max_value=300.0, step = 0.1, value = float(profile["general"]["weight"])
            )
        height = st.number_input(
            "Height (cm)", min_value=0.0, max_value=250.0, step = 0.1, value = float(profile["general"]["height"])
            )
        
        genders = ["Male","Female","Other"]
        gender = st.radio('Gender', genders, genders.index(profile["general"].get("gender", "Male")))
        
        activities = (
            "Sedentary",
            "Lightly Active",
            "Moderately Active",
            "Very Active",
            "Super Active"
        )

        activity_level = st.selectbox("Activity Level", activities, index = activities.index(profile["general"].get("activity_level","Sedentary")))

        personal_data_submit = st.form_submit_button("Save")
        if personal_data_submit:
            if all([name, age, weight, height, gender, activity_level]):
                with st.spinner():
                    st.session_state.profile = update_personal_info(
                        profile,
                        "general",
                        name = name,
                        weight = weight,
                        height = height,
                        gender = gender,
                        age = age,
                        activity_level = activity_level,
                    )
                    st.success("Information saved.")
            else:
                st.warning("Please fill in all of the data")

@st.fragment()
def goals_form():
    profile = st.session_state.profile
    with st.form("goals_form"):
        st.header("📌 Goals")
        goals = st.multiselect("Select your goals", ["Muscle Gain","Fat Loss","Stay Active"],
                               default=profile.get("goals",["Muscle Gain"]))
        
        goals_submit = st.form_submit_button("Save")
        if goals_submit:
            if goals:
                with st.spinner():
                    st.session_state.profile = update_personal_info(profile, "goals", goals = goals)
                    st.success("Goals updated")
            else:
                st.warning("Please select at least 1 goal")

@st.fragment()
def macros():
    profile = st.session_state.profile
    nutrition = st.container(border = True)
    nutrition.header("📌 Macro")
    if nutrition.button("Generate with AI"):
        result = get_macros(profile.get("general"), profile.get("goals"))
        profile["nutrition"] = result
        nutrition.success("AI has generated the results.")

    with nutrition.form("nutrition_form", border = False):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            calories = st.number_input(
                "Calories",
                min_value = 0, 
                step =1, 
                value = profile["nutrition"].get("calories", 0))
        with col2:
            protein = st.number_input(
                "Protein",
                min_value = 0, 
                step =1, 
                value = profile["nutrition"].get("protein", 0))
        with col3:
            fat = st.number_input(
                "Fat",
                min_value = 0, 
                step =1, 
                value = profile["nutrition"].get("fat", 0))            
        with col4:
            carbs = st.number_input(
                "Carbs",
                min_value = 0, 
                step =1, 
                value = profile["nutrition"].get("carbs", 0))
        
        if st.form_submit_button("Save"):
            with st.spinner():
                st.session_state.profile = update_personal_info(
                    profile, 
                    "nutrition", 
                    protein = protein,
                    calories = calories,
                    fat = fat,
                    carbs = carbs)
                st.success("Information saved")

@st.fragment()
def notes():
    st.subheader("📌 Notes: ")
    for i, note in enumerate(st.session_state.notes):
        cols = st.columns([5,1])
        with cols[0]:
            st.text(note)
        with cols[1]:
            if st.button("Delete", key = i):
                delete_note(i, st.session_state.profile_id)
                st.session_state.notes.pop(i)
                st.rerun(scope="fragment")
    new_note = st.text_input("Add a new note: ")
    if st.button("Add Note"):
        if new_note:
            note = add_note(new_note, st.session_state.profile_id)
            st.session_state.notes.append(note)
            st.rerun(scope="fragment")

@st.fragment()
def ask_ai_func():
    st.subheader("Ask AI")
    user_question = st.text_input("Ask AI a question: ")

    if st.button("Ask AI"):
        with st.spinner():
            result = ask_ai(st.session_state.profile, st.session_state.notes, user_question)
            st.write(result)

@st.fragment()
def chat_with_ai_bot():
    st.subheader("💬 Chat with your AI-powered fitness advisor")

    # Initialize or load chat history
    if "messages" not in st.session_state:
        st.session_state.messages = load_chat_history()

    if st.button("Delete Chat History"):
        st.session_state.messages = []
        save_chat_history([])

    # Display chat messages
    for message in st.session_state.messages:
        avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    prompt = st.chat_input("Hi, I am your fitness advisor. How can I help you today?")
    # Main chat interface
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar=USER_AVATAR):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar=BOT_AVATAR):
            message_placeholder = st.empty()
            full_response = ""
            stream = chat_with_ai(st.session_state.profile,st.session_state.notes,st.session_state.messages)
            for response in stream:
                full_response += response.choices[0].delta.content or ""
                message_placeholder.markdown(full_response + "|")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        st.rerun()

    # Save chat history after each interaction
    save_chat_history(st.session_state.messages)
    

def forms():
    if "profile" not in st.session_state:
        profile_id = 1
        try:
            profile = get_profile(profile_id)
        except:
            profile_id, profile = create_profile(profile_id)
        
        st.session_state.profile = profile
        st.session_state.profile_id = profile_id

    if "notes" not in st.session_state:
        try:
            st.session_state.notes = get_notes(st.session_state.profile_id)
        except:
            st.session_state.notes = []

    personal_data_form()
    goals_form()
    macros()
    notes()
    chat_with_ai_bot()
    
if __name__ == "__main__":
    forms()
