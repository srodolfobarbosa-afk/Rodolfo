Guia de Instalação do Chat SDK

Este guia detalha o processo de instalação e integração do Vercel AI Chat SDK no projeto Ecoguardin.

## 1. Configuração do Ambiente

Primeiro, é fundamental que o ambiente de desenvolvimento esteja pronto.

*   **Verificar Node.js:** O Chat SDK exige uma versão recente do Node.js (18 ou superior). O time pode verificar a versão com o comando `node -v` no terminal.
*   **Instalar gerenciador de pacotes:** O Chat SDK geralmente utiliza o `pnpm`, mas também funciona com `npm` ou `yarn`. Se o `pnpm` não estiver instalado, eles podem instalá-lo com `npm install -g pnpm`.
*   **Chave de API:** Para que o chatbot funcione, ele precisará se conectar a um modelo de IA. A equipe deve obter uma chave de API de um provedor como o Google Gemini ou OpenAI. Essa chave é como uma senha e deve ser armazenada em um arquivo de variáveis de ambiente (`.env`).

## 2. Instalação do Chat SDK

Com o ambiente pronto, a instalação é simples.

*   **Instalar o pacote:** Dentro do diretório do projeto, eles devem executar o comando para adicionar o SDK. O pacote principal é `ai`.

    ```bash
    pnpm add ai
    ```

    ou, se preferirem usar outro gerenciador:

    ```bash
    npm install ai
    ```

*   **Ajustar o arquivo .env:** Eles precisam adicionar a chave de API que obtiveram na etapa 1 ao arquivo `.env` na raiz do projeto, por exemplo:

    ```
    GOOGLE_API_KEY="SUA_CHAVE_AQUI"
    ```

    Obs: O nome da variável pode mudar dependendo do provedor de IA.

## 3. Integração com o Projeto Ecoguardin

A parte mais importante é incorporar a interface do chat ao código existente.

*   **Criar um componente de chat:** Eles podem criar um novo componente (por exemplo, `ChatComponent.js`) onde usarão o hook `useChat` do SDK. Esse hook gerencia o estado da conversa (mensagens, entrada do usuário, etc.).
*   **Adicionar o chat à interface:** Eles devem então importar o `ChatComponent` para a página onde o chat será exibido. Por exemplo, se o projeto usa React e Next.js, eles podem adicioná-lo ao arquivo `page.js` ou `layout.js`.
*   **Configurar o endpoint da API:** Para que o chat se comunique com o modelo de IA, eles precisam criar uma rota de API no backend do projeto. Essa rota será responsável por receber as mensagens do frontend, enviar para a API da IA e retornar a resposta.

Este guia oferece um roteiro claro para a equipe técnica. Se eles tiverem alguma dúvida, a documentação oficial do Chat SDK e tutoriais da Vercel no YouTube podem ser ótimos recursos.

