from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from google import genai
import chromadb
from sqlalchemy.orm import Session
from fastapi import File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import PyPDF2
import io
import time # 🔴 नया इम्पोर्ट: API को हैंग होने से बचाने के लिए

# अपनी SQL फाइल से चीज़ें इम्पोर्ट कीं
from database import ChatRecord, get_db

db_client = chromadb.PersistentClient(path="./my_data")
collection = db_client.get_or_create_collection(name="my_pdf_data")

ai_client = genai.Client(api_key="Enter you api key")

app = FastAPI(title="Proper AI Tool (Chat & PDF)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class userrequest(BaseModel):
    question: str

@app.post("/upload")
async def upload_user_pdf(file: UploadFile = File(...)):
    try:
        # 🔴 फिक्स 1: FastAPI से PDF को एकदम सेफ तरीके से पढ़ना
        pdf_bytes = await file.read()
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
        
        raw_text = ""
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                raw_text += text
                
        if not raw_text.strip():
            raise Exception("PDF में कोई टेक्स्ट नहीं मिला। (शायद यह स्कैन की हुई इमेज है)")

        # 2. TRANSFORM: टेक्स्ट को छोटे टुकड़ों (Chunks) में तोड़ना
        chunk_size = 1000
        chunks = [raw_text[i:i+chunk_size] for i in range(0, len(raw_text), chunk_size)]
        
        all_embeddings = []
        all_ids = []
        
        for i, chunk in enumerate(chunks):
            # 🔴 फिक्स 2: सही Embedding मॉडल का नाम 
            response = ai_client.models.embed_content(
                model="gemini-embedding-001",
                contents=chunk
            )
            all_embeddings.append(response.embeddings[0].values)
            all_ids.append(f"{file.filename}_chunk_{i+1}")
            
            # 🔴 फिक्स 3: API लिमिट (429 Error) से बचने के लिए 2 सेकंड का गैप
            time.sleep(2)
            
        # 3. LOAD: ChromaDB में डेटा सेव करना
        collection.add(
            documents=chunks,
            embeddings=all_embeddings,
            ids=all_ids
        )

        return {
            "filename": file.filename, 
            "message": "आपकी PDF सफलतापूर्वक डेटाबेस में सेव हो गई है! अब आप सवाल पूछ सकते हैं।"
        }
    except Exception as e:
        print("Backend Upload Error:", str(e)) # टर्मिनल में एरर दिखाने के लिए
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask")
async def ask_ai(data: userrequest, db: Session = Depends(get_db)):
    try:
        if collection.count() == 0:
            return {"ai_answer": "माफ़ कीजिएगा, मेरे पास अभी कोई डेटा नहीं है। कृपया पहले अपनी PDF अपलोड करें!"}
        
        user_question = data.question
        
        # 1. सवाल को नंबर्स (Embeddings) में बदलना
        response = ai_client.models.embed_content(
            model="gemini-embedding-001",
            contents=user_question
        )
        embedding_question = response.embeddings[0].values

        # 2. ChromaDB से PDF का डेटा ढूँढना
        db_search = collection.query(
            query_embeddings=[embedding_question],
            n_results=1
        )

        best_chunk = ""
        if db_search['documents'] and len(db_search['documents'][0]) > 0:
            best_chunk = db_search['documents'][0][0]

        # 3. स्मार्ट प्रॉम्प्ट
        prompt = f"""
        तुम एक बहुत ही समझदार और मददगार AI दोस्त हो। 
        
        नियम:
        1. सबसे पहले नीचे दिए गए 'PDF टेक्स्ट' में यूज़र के सवाल का जवाब ढूँढो। अगर मिल जाए, तो उसी के आधार पर जवाब दो।
        2. अगर जवाब 'PDF टेक्स्ट' में बिल्कुल नहीं है, तो तुम अपनी 'जनरल नॉलेज' से जवाब दे सकते हो। लेकिन यूज़र को प्यार से बता देना कि "यह जानकारी PDF में तो नहीं थी, लेकिन मैं बता देता हूँ..."
        
        PDF टेक्स्ट: {best_chunk}
        यूज़र का सवाल: {user_question}
        """

        # 🔴 फिक्स 4: सही AI मॉडल का इस्तेमाल (gemini-3-flash-preview हटाकर)
        final_response = ai_client.models.generate_content(
            model="gemini-3-flash-preview", 
            contents=prompt
        )
        ai_text = final_response.text

        # 5. बातचीत को SQL डेटाबेस में सेव करना
        new_chat = ChatRecord(
            user_message=user_question, 
            ai_response=ai_text
        )
        db.add(new_chat)
        db.commit()

        return {
            "status": "success",
            "question": user_question,
            "ai_answer": ai_text
        }
    
    except Exception as e:
        print("Backend Ask Error:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

# हिस्ट्री देखने का रूट
@app.get("/history")
async def get_chat_history(db: Session = Depends(get_db)):
    all_chats = db.query(ChatRecord).all()
    return {
        "total_messages": len(all_chats),
        "history": all_chats
    }