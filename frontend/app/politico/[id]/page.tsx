"use client";

import { use, useEffect, useState } from "react";
import Link from "next/link";

export default function DossiePolitico({ params }: { params: Promise<{ id: string }> }) {
  const resolvedParams = use(params);
  const idDoPolitico = resolvedParams.id;

  const [dados, setDados] = useState<any>(null);
  const [carregando, setCarregando] = useState(true);

  useEffect(() => {
    fetch(`http://localhost:8000/api/politicos/${idDoPolitico}`)
      .then((resposta) => resposta.json())
      .then((dadosDoApi) => {
        console.log("ESPIÃO DE DADOS:", dadosDoApi);
        setDados(dadosDoApi);
        setCarregando(false);
      })
      .catch((erro) => {
        console.error("Erro ao buscar detalhes:", erro);
        setCarregando(false);
      });
  }, [idDoPolitico]);

  return (
    <div className="min-h-screen bg-slate-50 p-8">
      {/* Botão de Voltar */}
      <div className="mb-6">
        <Link href="/" className="text-blue-600 hover:text-blue-800 font-medium flex items-center gap-2">
          ← Voltar para o Diretório
        </Link>
      </div>

      {carregando ? (
        <div className="text-center py-20 text-slate-500 animate-pulse text-xl">
          Montando dossiê confidencial...
        </div>
      ) : (
        <main className="bg-white p-8 rounded-xl shadow-sm border border-slate-200 max-w-4xl mx-auto">
          {/* Cabeçalho do Político - Agora buscando de dados.politico */}
          <header className="border-b border-slate-200 pb-6 mb-6">
            <h1 className="text-4xl font-bold text-slate-900 mb-2">{dados?.politico?.nome_urna || "Nome não encontrado"}</h1>
            <p className="text-xl text-slate-600">
              {dados?.politico?.cargo} • {dados?.politico?.partido} - {dados?.politico?.uf}
            </p>
          </header>

          {/* Área de Informações principais */}
          <div className="grid grid-cols-2 gap-8 mb-8">
            <div className="bg-slate-50 p-6 rounded-lg border border-slate-100 text-center">
              <h2 className="text-lg font-semibold text-slate-800 mb-2">Score de Coerência</h2>
              <p className={`text-5xl font-bold ${dados?.politico?.score_coerencia > 70 ? 'text-green-600' : 'text-red-600'}`}>
                {dados?.politico?.score_coerencia}%
              </p>
            </div>
            
            <div className="bg-slate-50 p-6 rounded-lg border border-slate-100">
              <h2 className="text-lg font-semibold text-slate-800 mb-2">Status da Análise</h2>
              <p className="text-slate-600">A IA do ContraDito identificou <strong>{dados?.provas?.length || 0}</strong> eventos recentes para análise de coerência.</p>
            </div>
          </div>

          {/* NOVA SEÇÃO: Lista de Provas/Contradições */}
          <section>
            <h2 className="text-2xl font-bold text-slate-800 mb-4 border-b pb-2">Evidências Encontradas</h2>
            
            <div className="space-y-4">
              {dados?.provas?.map((prova: any, index: number) => (
                <div key={index} className="border border-slate-200 rounded-lg p-4 hover:border-blue-300 transition-colors">
                  <div className="flex justify-between items-start mb-2">
                    <span className="bg-blue-100 text-blue-800 text-xs font-bold px-2.5 py-0.5 rounded uppercase">
                      {prova.informacao_extraida?.tipo_documento}
                    </span>
                    <span className="text-slate-400 text-sm">{prova.informacao_extraida?.data_evento}</span>
                  </div>
                  
                  <h3 className="font-bold text-slate-800 mb-1">{prova.resultado?.topico_identificado}</h3>
                  <p className="text-slate-600 italic mb-3">"{prova.informacao_extraida?.texto_extraido}"</p>
                  
                  <div className="bg-slate-50 p-3 rounded border-l-4 border-blue-500">
                    <p className="text-sm text-slate-700"><strong>Análise da IA:</strong> {prova.resultado?.justificativa}</p>
                    <p className="text-sm mt-2">
                        <strong>Postura:</strong> 
                        <span className="ml-1 font-medium">{prova.resultado?.postura_extraida_do_texto}</span>
                    </p>
                  </div>
                </div>
              ))}

              {(!dados?.provas || dados?.provas.length === 0) && (
                <p className="text-slate-500 text-center py-4">Nenhuma prova registrada para este parlamentar.</p>
              )}
            </div>
          </section>

        </main>
      )}
    </div>
  );
}