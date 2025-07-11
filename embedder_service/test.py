# METHOD 2: Level 3 Document-Based Chunking
# """Perform document-based chunking"""
# Source: https://github.com/FullStackRetrieval-com/RetrievalTutorials/blob/main/tutorials/LevelsOfTextSplitting/5_Levels_Of_Text_Splitting.ipynb
# filepath = "test"

# raw_pdf_elements = partition_pdf(
#     filename=filepath,
#     extract_images_in_pdf=True,
#     infer_table_structure=True,
#     chunking_strategy="by_title",
#     max_characters=4000,
#     new_after_n_chars=3800,
#     combine_text_under_n_chars=2000,
#     image_output_dir_path="static/pdfImages/",
# )

# markdown_text = """
# # Fun in California

# ## Driving

# Try driving on the 1 down to San Diego

# ### Food

# Make sure to eat a burrito while you're there

# ## Hiking

# Go to Yosemite
# """

# try:
#     chunks = document_chunker.create_documents([markdown_text])
#     logger.info("Number of chunks:", len(chunks))

#     # # Reject by returning empty list if PDF document has no content
#     if not markdown_text.strip():
#         raise HTTPException(status_code=400, detail="No text content found in PDF")

#     chunk_data = []
#     current_pos = 0

#     for i, chunk in enumerate(chunks):
#         # First iteration: Extract first chunk of doc.page_content
#         chunk_content = chunk.page_content
#         logger.info(f"Length of chunk {i+1}:", len(chunk_content.strip()))
#         # First iteration: Start from first chunk of doc.page_context
#         chunk_start = markdown_text.find(chunk_content, current_pos)

#         if chunk_start == -1:
#             chunk_start = current_pos

#         chunk_end = chunk_start + len(chunk_content)

#         # # Find which page this chunk belongs to
#         # page_number = None
#         # for page_info in request.pages_info:
#         #     if (chunk_start >= page_info['char_start'] and
#         #             chunk_start < page_info['char_end']):
#         #         page_number = page_info['page_number']
#         #         break

        # "metadata": {
            #     "text_chunk_key": f"text_chunk_{page_number + 1}_{chunk_idx + 1}",
            #     "type": "text",
            # },

#         # Skip chunks that are too small or too large (if necessary)
#         # if (len(chunk_content.strip()) < request.config.min_chunk_size) or (len(chunk_content.strip()) > request.config.max_chunk_size):
#         #     current_pos = chunk_end
#         #     continue

#         # else:
#         chunk_data.append({
#         'chunk_id': str(uuid.uuid4()),
#         'content': chunk_content.strip(),
#         'start_char': chunk_start,
#         'end_char': chunk_end,
#         'page_number': None,
#         'chunk_index': len(chunk_data),
#         'metadata': chunk.metadata
#         })

#         current_pos = chunk_end

#     logger.info("Chunk data:", chunk_data)
#     return chunk_data

# except Exception as e:
#     logger.error(f"Document-based chunking failed: {e}")


# Global instances
# embedding_model = None
# semantic_chunker = None
# document_chunker = None
# chroma_client = None

# Global instances
# embedding_model = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
# embedding_model = SentenceTransformer(DataRequest.config.embedding_model)
# embeddings_instance = SentenceTransformerEmbeddings(DataRequest.config.embedding_model)
# semantic_chunker = SemanticChunker(embeddings_instance, breakpoint_threshold_type="percentile", breakpoint_threshold_amount=90)
# document_chunker = MarkdownTextSplitter(chunk_size = 40, chunk_overlap=0)
# chroma_client = chromadb.Client() # data stored in memory, not on disk

# global embedding_model, chroma_client, semantic_chunker
    # # global document_chunker

    # if embedding_model is None:
    #     logger.info("Loading embedding model...")
    #     # embedding_model = SentenceTransformer(request.config.embedding_model)
    #     embedding_model = SentenceTransformerEmbeddings(request.config.embedding_model)
    #     logger.info(request.config.embedding_model)

    # # Semantic Chunking
    # if semantic_chunker is None:
    #     logger.info("Initializing semantic chunker...")
    #     semantic_chunker = SemanticChunker(embedding_model, breakpoint_threshold_type="percentile", breakpoint_threshold_amount=90)

    # # Alternative: Document-Based Chunking
    # # if document_chunker is None:
    # #     logger.info("Initializing document-based chunker...")
    # #     document_chunker = MarkdownTextSplitter(chunk_size = 40, chunk_overlap=0)

    # if chroma_client is None:
    #     logger.info("Initializing ChromaDB client...")
    #     chroma_client = chromadb.Client() # data stored in memory, not on disk


# class RAGHelper:
#     """Helper for Retrieval Augmented Generation (RAG)."""

#     def __init__(self):
#         self.message = "Hello World, I am a helper class for RAG."
#         embedding_function = NomicEmbeddings(
#             model="text-embedding-nomic-embed-text-v1.5-embedding"
#         )
#         chromadb.api.client.SharedSystemClient.clear_system_cache()  # Clear cache to handle "could not connect to tenant default_tenant" error
#         self.vectorstore = Chroma("all_documents", embedding_function)

#     def get(self) -> str:
#         return self.message

#     def get_all_documents(self) -> List[Document]:
#         if self.vectorstore:
#             return self.vectorstore.get()

#     def add_docs_to_chromadb(self, docs: list[dict]) -> None:
#         if self.vectorstore:
#             self.vectorstore.reset_collection()

#         # Convert to Document type
#         docs = [
#             Document(page_content=doc["page_content"], metadata=doc["metadata"])
#             for doc in docs
#         ]
#         return self.vectorstore.add_documents(docs)

#     def retrieve_relevant_docs(self, user_query: str, top_k: int) -> list[Document]:
#         """Retrieve relevant documents from vector database based on user
#         query.

#         Parameters
#         ----------
#         user_query : str
#             The user query or prompt in "Chat with Omni".

#         Returns
#         -------
#         pd.DataFrame
#             The DataFrame that contains the documents with relevance score.
#         """

#         # Read vector database as DataFrame
#         results = self.vectorstore.similarity_search(
#             user_query,
#             k=top_k,
#         )

#         # Retrieve relevant docs
#         return results

# RAGGING (part of chat service)
# def rag(chunks, collection_name):
#     # Load all data chunks into ChromaDB
#     vectorstore = Chroma.from_documents(
#         documents=documents,
#         collection_name=collection_name,
#         # embedding=Embeddings.ollama.OllamaEmbeddings(model='nomic-embed-text'),
#         embedding=Embeddings,
#     )
#     # To check ChromaDB
#     retriever = vectorstore.as_retriever()

#     prompt_template = """Answer the question based only on the following context:
#     {context}
#     Question: {question}
#     """
#     prompt = ChatPromptTemplate.from_template(prompt_template)

#     chain = (
#         {"context": retriever, "question": RunnablePassthrough()}
#         | prompt
#         | local_llm
#         | StrOutputParser()
#     )

#     # User prompt
#     result = chain.invoke("What is the use of Text Splitting?")
#     logger.info(result)


# async def query_chromadb(user_query, collection_name, emb_model, top_k) -> Dict[str, Any]:
#     """
#     Query the ChromaDB collection for relevant documents.
#     """
    
#     try:        
#         # Get the collection
#         collection = chroma_client.get_collection(
#             name=collection_name,
#             embedding_function=emb_model
#         )
        
#         # Query the collection
#         results = await run_in_threadpool(
#             collection.query,
#             query_texts=[user_query],
#             n_results=top_k,
#             include=["distances", "documents", "metadatas"]
#         )
        
#         return results
    
#     except Exception as e:
#         logger.error(f"ChromaDB query failed: {e}")
#         raise HTTPException(status_code=500, detail="Database query failed")


# def format_chunks_for_llm(results: Dict[str, Any], max_context_length: int = 4000) -> tuple[List[Dict[str, Any]], str]:
#     """Format ChromaDB results for Qwen-2.5 with context length optimization"""
#     formatted_chunks = []
#     context_text = ""
    
#     if not results or not results.get('documents'):
#         return formatted_chunks, context_text
    
#     documents = results['documents'][0] if results['documents'] else []
#     metadatas = results['metadatas'][0] if results['metadatas'] else []
#     distances = results['distances'][0] if results['distances'] else []
    
#     context_parts = []
#     current_length = 0
    
#     for i, doc in enumerate(documents):
#         chunk_data = {
#             'content': doc,
#             'metadata': metadatas[i] if i < len(metadatas) else {},
#             'similarity_score': 1 - distances[i] if i < len(distances) else 0,
#             'rank': i + 1
#         }
#         formatted_chunks.append(chunk_data)
        
#         # Build context for Qwen-2.5 with length management
#         chunk_text = f"[Document Section {i+1}]:\n{doc}\n"
        
#         # Check if adding this chunk would exceed context limit
#         if current_length + len(chunk_text) > max_context_length:
#             logger.info(f"Context limit reached, using top {i} chunks")
#             break
            
#         context_parts.append(chunk_text)
#         current_length += len(chunk_text)
    
#     context_text = "\n".join(context_parts)
#     return formatted_chunks, context_text


# async def generate_rag_response(
#     question: str, 
#     context: str, 
#     client: OpenAI,
#     query_type: str = "general"
# ) -> str:
#     """Generate RAG-enhanced response using Qwen-2.5 with optimized prompting"""
    
#     # Get Qwen-2.5 optimized prompts
#     system_prompt = prompt_templates.get_system_prompt(query_type)
#     user_prompt = prompt_templates.format_user_prompt(question, context, query_type)
    
#     try:
#         response = await run_in_threadpool(
#             client.chat.completions.create,
#             model=qwen_config.model_name,
#             messages=[
#                 {"role": "system", "content": system_prompt},
#                 {"role": "user", "content": user_prompt}
#             ],
#             **qwen_config.generation_params
#         )
        
#         if not response.choices or not response.choices[0].message:
#             raise ValueError("Invalid response from Qwen-2.5")
            
#         raw_response = response.choices[0].message.content
        
#         # Post-process response for better formatting
#         if os.getenv("ENABLE_RESPONSE_POST_PROCESSING", "true").lower() == "true":
#             processed_response = qwen_optimizer.post_process_qwen_response(raw_response, question)
#             return processed_response
        
#         return raw_response
        
#     except Exception as e:
#         logger.error(f"Qwen-2.5 response generation failed: {e}")
#         raise


# # For local testing purposes
# async def handle_chat(
#     emb_model,
#     chat_request: ChatRequest,
#     client: OpenAI = Depends(get_openai_client),
# ) -> ChatResponse:
#     """
#     Handle RAG-based chat requests with document context retrieval.
#     """
#     try:
#         # # Verify document ownership
#         # if not await verify_document_ownership(chat_request.id):
#         #     raise HTTPException(
#         #         status_code=403, 
#         #         detail="Access denied: Document ownership verification failed"
#         #     )
        
#         # Detect query type if not provided
#         query_type = chat_request.query_type
#         if not query_type and os.getenv("ENABLE_QUERY_TYPE_DETECTION", "true").lower() == "true":
#             query_type = qwen_optimizer.detect_query_type(chat_request.message)
#         else:
#             query_type = query_type or "general"
        
#         logger.info(f"Processing RAG chat request for doc_id: {chat_request.id}, query_type: {query_type}")
        
#         # Query ChromaDB for relevant chunks
#         results = await query_chromadb(
#             chat_request.message,
#             chat_request.collection_name,
#             emb_model,
#             chat_request.top_k
#         )
        
#         # Optimize chunks using Qwen-2.5 specific optimization
#         relevant_chunks, context_text = qwen_optimizer.optimize_chunks_for_qwen(
#             format_chunks_for_llm(results),
#             max_context_length=qwen_config.max_context_length
#         )
        
#         if not relevant_chunks:
#             raise HTTPException(
#                 status_code=404,
#                 detail="No relevant content found in the document for your question"
#             )
        
#         # Generate RAG-enhanced response using Qwen-2.5
#         rag_response = await generate_rag_response(
#             question=chat_request.message,
#             context=context_text,
#             client=client,
#             query_type=query_type
#         )
        
#         # Prepare response metadata
#         metadata = {
#             "total_chunks_found": len(relevant_chunks),
#             "collection_name": chat_request.collection_name,
#             "top_k_requested": chat_request.top_k,
#             "model_used": qwen_config.model_name,
#             "query_type": query_type,
#             "context_length": len(context_text),
#             "generation_params": qwen_config.generation_params,
#             "request_id": chat_request.id
#         }
        
#         logger.info(f"Successfully processed RAG chat request for doc_id: {chat_request.id}")
        
#         return ChatResponse(
#             response=rag_response,
#             relevant_chunks=relevant_chunks,
#             metadata=metadata
#         )
        
#     except HTTPException:
#         raise
#     except APIError as e:
#         logger.error(f"OpenAI API error during chat: {e}", exc_info=True)
#         raise HTTPException(status_code=500, detail="AI service error")
#     except Exception as e:
#         logger.error(f"Unexpected error during chat: {e}", exc_info=True)
#         raise HTTPException(status_code=500, detail="Internal server error")