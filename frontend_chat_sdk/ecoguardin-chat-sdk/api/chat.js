import { GoogleGenerativeAI } from '@google/generative-ai';
import { GoogleGenerativeAIStream, Message, StreamingTextResponse } from 'ai';

const genAI = new GoogleGenerativeAI(process.env.GOOGLE_API_KEY || '');

export const runtime = 'edge';

export async function POST(req) {
  const { messages } = await req.json();

  const model = genAI.getGenerativeModel({ model: 'gemini-pro' });

  const stream = GoogleGenerativeAIStream(model, {
    onStart: async () => {
      // This callback is called when the stream starts
      // You can use it to log the messages or perform other actions
      console.log('Stream started with messages:', messages);
    },
    onToken: async (token) => {
      // This callback is called for each token in the stream
      // You can use it to log the tokens or perform other actions
      console.log('Token received:', token);
    },
    onFinal: async (completion) => {
      // This callback is called when the stream ends
      // You can use it to log the completion or perform other actions
      console.log('Stream completed with completion:', completion);
    },
  });

  return new StreamingTextResponse(stream);
}

