import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Engelsk B Træning", layout="wide")

adgangskode = st.text_input("Indtast adgangskode", type="password")

if adgangskode == "1531":
    api_key = st.secrets["API_KEY"]

    if api_key:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')

        st.title("Engelsk B Eksamensforberedelse")
        
        tab1, tab2, tab3, tab4 = st.tabs(["Grammatik og Ordforråd", "Afsnitstræning", "Essay Værksted", "Flashcards"])

        with tab1:
            st.write("Generer en tilfældig grammatik- eller bindeordsopgave på Engelsk B-niveau.")
            if st.button("Generer ny opgave"):
                prompt = "Du er engelsklærer for en gymnasieelev. Lav én kort opgave hvor eleven enten skal indsætte et manglende bindeord (linker) i en sætning, eller finde og rette en specifik grammatisk fejl. Giv kun selve opgaven, ikke svaret."
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
            st.write("Få en skriveøvelse eller indsæt et afsnit for at få tjekket sprog, struktur og begreber.")
            
            if st.button("Få en skriveøvelse (Inspiration)"):
                prompt = "Du er engelsklærer. Giv eleven en kort og specifik skriveøvelse til at træne et analytisk afsnit på Engelsk B. Opfind et fiktivt emne, fx 'skriv et afsnit der analyserer fortælleren i en novelle', og foreslå 3 specifikke engelske analytiske begreber eller bindeord, der bør indgå. Skriv det kort og præcist på dansk."
                response = model.generate_content(prompt)
                st.session_state['skriveoevelse'] = response.text
                
            if 'skriveoevelse' in st.session_state:
                st.write("Din opgave:")
                st.write(st.session_state['skriveoevelse'])

            afsnit = st.text_area("Dit afsnit:", height=150)
            fokusord = st.text_input("Hvilke analytiske begreber eller bindeord har du forsøgt at bruge?")
            
            if st.button("Analyser afsnit"):
                prompt = f"Du er sprogkonsulent. Evaluér følgende afsnit skrevet af en dansk gymnasieelev på Engelsk B-niveau. Eleven har forsøgt at inddrage disse ord: {fokusord}. Afsnit: {afsnit}. Vurder om ordene er brugt i korrekt kontekst. Giv feedback på syntaks, vurdér afsnittets logiske struktur (fx ift. PEEL-strukturen), og kom med 3 konkrete forslag til at gøre sproget mere akademisk."
                response = model.generate_content(prompt)
                st.write(response.text)

        with tab3:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write("Skriveområde og Censor")
                if st.button("Generer et nyt essay-oplæg"):
                    prompt = "Lav et kort, realistisk essay-oplæg til Engelsk B (STX). Angiv et overordnet emne (fx non-fiction, fiction, literature) og 3 specifikke analytiske punkter, eleven skal inddrage. Skriv oplægget på engelsk, præcis som i en eksamensopgave."
                    response = model.generate_content(prompt)
                    st.session_state['essay_oplaeg'] = response.text
                    
                if 'essay_oplaeg' in st.session_state:
                    st.write(st.session_state['essay_oplaeg'])

                essay = st.text_area("Dit essay:", height=500)
                
                if st.button("Bedøm essay"):
                    prompt = f"Du er ekstern censor til skriftlig eksamen i Engelsk B på STX i Danmark. Analysér følgende essay ud fra de officielle ministerielle krav: sproglig korrekthed, sammenhæng, tekstanalyse og struktur. Giv konstruktiv kritik på dansk opdelt i: 1) Styrker, 2) Sproglige fokuspunkter (genkommende fejl), og 3) En vurdering af det faglige niveau. Essay: {essay}"
                    response = model.generate_content(prompt)
                    st.write(response.text)
                    
            with col2:
                st.write("Ordbog og Inspiration")
                opslaagsord = st.text_input("Oversæt et dansk ord til akademisk engelsk:")
                if st.button("Slå op"):
                    prompt = f"Oversæt det danske ord '{opslaagsord}' til engelsk. Giv det mest præcise ord, samt 2 gode synonymer der hæver niveauet i et Engelsk B essay. Svar kort på dansk uden overskrifter."
                    response = model.generate_content(prompt)
                    st.write(response.text)
                    
                st.write("")
                st.write("")
                
                if st.button("Få 5 gode vendinger til dit emne"):
                    if 'essay_oplaeg' in st.session_state:
                        prompt = f"Eleven skal skrive et essay om følgende emne: {st.session_state['essay_oplaeg']}. Giv 5 akademiske engelske bindeord eller analytiske vendinger, der vil passe perfekt til at løse netop denne opgave. Giv en ultrakort dansk forklaring til hver."
                        response = model.generate_content(prompt)
                        st.write(response.text)
                    else:
                        st.write("Du skal generere et essay-oplæg først.")

        with tab4:
            st.write("Træn analytiske begreber, bindeord og akademiske udsagnsord fra ordlisten.")
            
            if st.button("Træk et nyt ord"):
                prompt = 'Giv mig ét tilfældigt dansk ord eller kort begreb relevant for skriftlig Engelsk B (fx et bindeord, litterært begreb eller akademisk udsagnsord) og dets engelske oversættelse. Formatér svaret præcis sådan her uden andet tekst: "dansk ord = engelsk ord".'
                response = model.generate_content(prompt)
                
                try:
                    dansk, engelsk = response.text.split("=")
                    st.session_state['flashcard_dk'] = dansk.strip()
                    st.session_state['flashcard_eng'] = engelsk.strip().lower()
                except:
                    st.write("Der opstod en fejl ved generering af ordet. Tryk igen.")
                    
            if 'flashcard_dk' in st.session_state:
                st.write(f"Hvad hedder dette på engelsk: {st.session_state['flashcard_dk']}")
                oversaettelse = st.text_input("Din oversættelse:", key="flashcard_input")
                
                if st.button("Tjek oversættelse"):
                    tjek_prompt = f"Eleven oversatte det danske ord '{st.session_state['flashcard_dk']}' til engelsk som '{oversaettelse}'. Det mest oplagte svar er '{st.session_state['flashcard_eng']}'. Vurder om elevens svar er korrekt eller et acceptabelt synonym i en akademisk Engelsk B kontekst. Svar kort og præcist på dansk."
                    tjek_response = model.generate_content(tjek_prompt)
                    st.write(tjek_response.text)

    else:
        st.write("API-nøgle mangler i Streamlit secrets.")
