import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Engelsk B Træning", layout="wide")

adgangskode = st.text_input("Indtast adgangskode", type="password")

if adgangskode == "1531":
    api_key = st.secrets["API_KEY"]

    if api_key:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-pro-latest')

        st.title("Engelsk B Eksamensforberedelse")
        
        tab1, tab2, tab3 = st.tabs(["Grammatik og Ordforråd", "Afsnitstræning", "Essay Censor"])

        with tab1:
            st.write("Generer en tilfældig grammatik- eller bindeordsopgave på Engelsk B-niveau.")
            if st.button("Generer ny opgave"):
                prompt = "Du er engelsklærer for en 1.g elev. Lav én kort opgave hvor eleven enten skal indsætte et manglende bindeord (linker) i en sætning, eller finde og rette en specifik grammatisk fejl. Giv kun selve opgaven, ikke svaret."
                response = model.generate_content(prompt)
                st.session_state['opgave'] = response.text
                
            if 'opgave' in st.session_state:
                st.write(st.session_state['opgave'])
                svar = st.text_input("Dit svar:")
                if st.button("Tjek svar"):
                    tjek_prompt = f"Opgaven var: {st.session_state['opgave']}. Elevens svar er: {svar}. Fortæl eleven om det er korrekt, og forklar reglen kort og pædagogisk på dansk."
                    tjek_response = model.generate_content(tjek_prompt)
                    st.write(tjek_response.text)

        with tab2:
            st.write("Indsæt et afsnit for at få tjekket sprog og brug af analytiske begreber.")
            afsnit = st.text_area("Dit afsnit:", height=150)
            fokusord = st.text_input("Hvilke analytiske begreber eller bindeord har du forsøgt at bruge?")
            
            if st.button("Analyser afsnit"):
                prompt = f"Du er sprogkonsulent. Evaluér følgende afsnit skrevet af en dansk gymnasieelev på Engelsk B-niveau. Eleven har forsøgt at inddrage disse ord: {fokusord}. Afsnit: {afsnit}. Vurder om ordene er brugt i korrekt kontekst. Giv feedback på syntaks og kom med 3 konkrete forslag til at gøre sproget mere akademisk."
                response = model.generate_content(prompt)
                st.write(response.text)

        with tab3:
            st.write("Få en fuld vurdering af dit essay (Opgave 5).")
            essay = st.text_area("Dit essay:", height=300)
            
            if st.button("Bedøm essay"):
                prompt = f"Du er ekstern censor til skriftlig eksamen i Engelsk B på STX i Danmark. Analysér følgende essay ud fra de officielle ministerielle krav: sproglig korrekthed, sammenhæng, tekstanalyse og struktur. Giv konstruktiv kritik på dansk opdelt i: 1) Styrker, 2) Sproglige fokuspunkter (genkommende fejl), og 3) En vurdering af det faglige niveau. Essay: {essay}"
                response = model.generate_content(prompt)
                st.write(response.text)

    else:
        st.write("API-nøgle mangler i Streamlit secrets.")
