from rag.ingest import split_documents

def test_split_documents_respects_chunk_size():
    texto_longo = 'palavra' *500
    chunks=split_documents([texto_longo])

    assert len(chunks)>1
    assert all(len(c) <=1000 for c in chunks)

def test_split_documents_overlap():
    texto = 'abcdefghij'*200 #2000 caracteres
    chunks = split_documents([texto],chunk_size=1000,chunk_overlap=200)

    #o final de um chunk deve aparece no início do próximo
    assert chunks[0][-50:] in chunks[1]

def test_split_documents_empty_input():
    chunks = split_documents([])
    assert chunks==[]

def test_split_documents_multiple_docs():
    doc1='conteúdo do primeiro pdf'*50
    doc2='conteúdo do segundo pdf'*50
    chunks = split_documents([doc1,doc2])

    assert any('primeiro' in c for c in chunks)
    assert any('segundo' in c for c in chunks)