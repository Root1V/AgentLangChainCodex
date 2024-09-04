import os
from dotenv import load_dotenv
import streamlit as st
import datetime
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_experimental.tools import PythonREPLTool
from model.config import Config


class App:
    """
    Clase que representa la aplicación de un agente de inteligencia artificial
    diseñado para responder preguntas sobre programación utilizando código Python.
    """

    def __init__(self) -> None:
        """
        Inicializa la aplicación cargando la configuración y definiendo el archivo
        donde se guardará el historial de interacciones.

        Attributes:
            config (dict): Configuración cargada desde el archivo de configuración.
            historyFile (str): Nombre del archivo que almacena el historial de preguntas y respuestas.
        """
        self.config = Config.get_all()
        self.historyFile = "history.txt"

    def save_history(self, question, answer):
        """
        Guarda una pregunta y su respuesta en el historial.

        Args:
            question (str): La pregunta realizada al agente.
            answer (str): La respuesta proporcionada por el agente.
        """
        with open(self.historyFile, "a") as h:
            h.write(f"{datetime.datetime.now()}: {question} -> {answer}\n")

    def load_history(self):
        """
        Carga el historial de preguntas y respuestas desde el archivo.

        Returns:
            list: Una lista de las líneas del historial. Si el archivo no existe,
            devuelve una lista vacía.
        """
        if os.path.exists(self.historyFile):
            with open(self.historyFile, "r") as h:
                return h.readlines()
        return []

    def clear_history(self):
        """
        Limpia el historial de preguntas y respuestas, vaciando el archivo correspondiente.
        """
        if os.path.exists(self.historyFile):
            open(self.historyFile, "w").close()

    def download_file(self):
        """
        Lee el contenido del archivo de historial y lo devuelve.

        Returns:
            str: Contenido del archivo de historial.
        """
        with open(self.historyFile, "r") as f:
            file_contents = f.read()
        return file_contents

    def agen_run(self, agent_executor, user_input):
        """
        Ejecuta el agente con la entrada del usuario, muestra la respuesta y guarda
        la interacción en el historial.

        Args:
            agent_executor (AgentExecutor): El ejecutor del agente que procesa la entrada.
            user_input (str): La entrada proporcionada por el usuario.
        """
        answer = agent_executor.invoke(input={"input": user_input})
        st.markdown("### Respuesta del Agente AI")
        st.code(answer["output"], language="python")
        self.save_history(user_input, answer["output"])

    def run(self):
        """
        Configura y ejecuta la interfaz de usuario de la aplicación utilizando Streamlit.
        Carga el prompt del agente, configura los botones y maneja las interacciones del usuario.
        """

        st.set_page_config(
            page_title="Agente AI para Codigo de Programación",
            page_icon="",
            layout="wide",
        )

        st.title("Agent AI Codex")
        st.markdown(
            """
            <style>
            .title { color: #1B69F0; }
            .button { background-color: #ff4b4b; color: white; border-radius: 5px;}
            .input { border: 1px solid #ff4b4b; border-radius: 5px;}
            </style>
            """,
            unsafe_allow_html=True,
        )

        prompt_system = """
            - Eres un agent de AI experto en programación con amplio conocimiento de buenas practicas y principios de diseño de software
            - Debes de usar siempre el codigo de python para responder.
            - Solo responder a la pregunta escribiendo codigo, incluso si sabes la respuesta.
            - Si no sabes la respuesta, responde "no se la respuesta"
        """

        st.markdown("### Instrucciones:")
        st.markdown(prompt_system)

        base_prompt = hub.pull("langchain-ai/react-agent-template")
        print("\nPrint prompt AI Agent React:", base_prompt)

        prompt = base_prompt.partial(instructions=prompt_system)
        st.write("Prompt base cargado...")

        tools = [PythonREPLTool()]
        llm = ChatOpenAI(
            model=self.config["model"], temperature=self.config["temperature"]
        )

        # Crear el agente
        agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

        # Ejecutar con ejemplos
        st.markdown("### Ejemplos:")
        examples = [
            "Calcula la division de 1234/5678",
            "Genera una lista con los 15 primeros numeros primos",
            "Crea una funcion que calcule el factorial del numero",
            "Calcula el factorial del numero 19",
        ]
        examp = st.selectbox("Selecciona un ejemplo:", examples)

        if st.button("Ejecutar ejemplo"):
            user_input = examp
            self.agen_run(agent_executor, user_input)

        # Capturar el input del usuario.
        user_input = st.text_input(
            "Introduce tu pregunta para el agente:", key="input_text"
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            exec = st.button("Ejecutar", key="exec_button")
        with col2:
            clean = st.button("Limpiar historial", key="clear_button")
        with col3:
            download = st.download_button(
                "Descargar historial",
                key="down_button",
                data=self.download_file(),
                file_name="full_history.txt",
            )

        if exec:
            if user_input:
                self.agen_run(agent_executor, user_input)
            else:
                st.warning("Ingresa una pregunta para el Agente AI")

        if clean:
            self.clear_history()

        if download:
            st.write("Descarga exitosa...")

        st.markdown("### Historial de consultas")
        history = self.load_history()
        if history:
            for h in history:
                st.text(h)
        else:
            st.write("No hay historial....")


if __name__ == "__main__":
    # Cargar las variables de entorno
    load_dotenv()
