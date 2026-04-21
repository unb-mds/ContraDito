"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";

export default function Home() {
  const [politicos, setPoliticos] = useState([]);
  const [carregando, setCarregando] = useState(true);
  
  const [textoBusca, setTextoBusca] = useState("");
  const [partidoSelecionado, setPartidoSelecionado] = useState("");
  const [ufSelecionada, setUfSelecionada] = useState("");
  const [ordemSelecionada, setOrdemSelecionada] = useState("");

  const [filtrosAtivos, setFiltrosAtivos] = useState({
    busca: "",
    partido: "",
    uf: "",
    ordem: ""
  });

  const router = useRouter();

  useEffect(() => {
    setCarregando(true);
    
    const params = new URLSearchParams();
    if (filtrosAtivos.busca) params.append("busca", filtrosAtivos.busca);
    if (filtrosAtivos.partido) params.append("partido", filtrosAtivos.partido);
    if (filtrosAtivos.uf) params.append("uf", filtrosAtivos.uf);
    if (filtrosAtivos.ordem) params.append("ordem", filtrosAtivos.ordem);

    const url = `http://localhost:8000/api/politicos?${params.toString()}`;

    fetch(url)
      .then((resposta) => resposta.json())
      .then((dados) => {
        setPoliticos(dados.itens || []);
        setCarregando(false);
      })
      .catch((erro) => {
        console.error("Erro ao buscar políticos:", erro);
        setCarregando(false);
      });
  }, [filtrosAtivos]);

  const executarBusca = () => {
    setFiltrosAtivos({
      busca: textoBusca,
      partido: partidoSelecionado,
      uf: ufSelecionada,
      ordem: ordemSelecionada
    });
  };

  return (
    <div className="min-h-screen bg-slate-50 p-8">
      
      {/* 1. NOVA CAPA IMERSIVA (HERO SECTION) */}
      <div className="relative bg-slate-900 text-white rounded-2xl overflow-hidden mb-8 shadow-2xl">
        <div className="absolute inset-0">
          <img 
            src="https://images.unsplash.com/photo-1620662736427-b8a198f52a4d?q=80&w=2070&auto=format&fit=crop" 
            alt="Congresso Nacional" 
            className="w-full h-full object-cover opacity-20"
          />
          <div className="absolute inset-0 bg-gradient-to-b from-transparent to-slate-900/90"></div>
        </div>

        <div className="relative z-10 px-8 py-24 flex flex-col items-start max-w-4xl mx-auto text-center md:text-left">
          <div className="inline-block bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider mb-6">
            Transparência Política com IA
          </div>
          
          <h1 className="text-5xl md:text-7xl font-bold mb-6 leading-tight tracking-tight text-white">
            O que foi dito <br/>
            <span className="text-emerald-400 italic font-serif">vs.</span> o que foi votado.
          </h1>
          
          <p className="text-lg md:text-xl text-slate-300 max-w-2xl mb-10 leading-relaxed">
            O <strong className="text-white">ContraDito</strong> usa Inteligência Artificial para cruzar discursos e votos de deputados e senadores, gerando um <strong className="text-emerald-400">Score de Coerência</strong> real.
          </p>

          <div className="flex flex-wrap gap-4">
            <button 
              onClick={() => window.scrollTo({ top: 600, behavior: 'smooth' })}
              className="bg-emerald-600 hover:bg-emerald-500 text-white px-8 py-3 rounded-full font-medium transition-all shadow-lg shadow-emerald-900/20"
            >
              Ver Políticos
            </button>
            <button className="bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 px-8 py-3 rounded-full font-medium transition-all">
              Entender a Metodologia
            </button>
          </div>
        </div>
      </div>

      {/* 2. FAIXA DE ESTATÍSTICAS GERAIS */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-10">
        <div className="bg-slate-900 rounded-2xl p-8 flex flex-col items-center justify-center border border-slate-800 shadow-xl transition-transform hover:-translate-y-1">
          <span className="text-emerald-400 text-4xl mb-3">🏛️</span>
          <h3 className="text-4xl font-bold text-white tracking-tight">513</h3>
          <p className="text-slate-400 text-sm mt-2 uppercase tracking-wider font-medium text-center">Deputados Federais</p>
        </div>

        <div className="bg-slate-900 rounded-2xl p-8 flex flex-col items-center justify-center border border-slate-800 shadow-xl transition-transform hover:-translate-y-1">
          <span className="text-emerald-400 text-4xl mb-3">🏛️</span>
          <h3 className="text-4xl font-bold text-white tracking-tight">81</h3>
          <p className="text-slate-400 text-sm mt-2 uppercase tracking-wider font-medium text-center">Senadores</p>
        </div>

        <div className="bg-slate-900 rounded-2xl p-8 flex flex-col items-center justify-center border border-slate-800 shadow-xl transition-transform hover:-translate-y-1">
          <span className="text-emerald-400 text-4xl mb-3">🎙️</span>
          <h3 className="text-4xl font-bold text-white tracking-tight">48.720</h3>
          <p className="text-slate-400 text-sm mt-2 uppercase tracking-wider font-medium text-center">Discursos Analisados</p>
        </div>

        <div className="bg-slate-900 rounded-2xl p-8 flex flex-col items-center justify-center border border-slate-800 shadow-xl transition-transform hover:-translate-y-1">
          <span className="text-emerald-400 text-4xl mb-3">📊</span>
          <h3 className="text-4xl font-bold text-white tracking-tight">71%</h3>
          <p className="text-slate-400 text-sm mt-2 uppercase tracking-wider font-medium text-center">Média de Coerência</p>
        </div>
      </div>

      {/* 3. ÁREA DE BUSCA E TABELA */}
      <main className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
        <h2 className="text-xl font-semibold text-slate-800 mb-4">
          Diretório de Políticos
        </h2>
        
        <div className="bg-slate-100 p-4 rounded-lg mb-6 border border-slate-200 flex flex-col gap-4">
          <div className="flex gap-4">
            <input 
              type="text" 
              placeholder="Buscar por nome de urna..." 
              className="flex-1 p-2 rounded border border-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-500 text-slate-800"
              value={textoBusca}
              onChange={(e) => setTextoBusca(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && executarBusca()}
            />
            <button 
              onClick={executarBusca}
              className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-8 rounded transition-colors"
            >
              Pesquisar
            </button>
          </div>

          <div className="flex gap-4">
            <select 
              className="p-2 rounded border border-slate-300 bg-white text-slate-700 flex-1 focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={partidoSelecionado}
              onChange={(e) => setPartidoSelecionado(e.target.value)}
            >
              <option value="">Todos os Partidos</option>
              <option value="PL">PL</option>
              <option value="PT">PT</option>
              <option value="MDB">MDB</option>
              <option value="PSDB">PSDB</option>
              <option value="NOVO">NOVO</option>
              <option value="PSOL">PSOL</option>
            </select>

            <select 
              className="p-2 rounded border border-slate-300 bg-white text-slate-700 flex-1 focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={ufSelecionada}
              onChange={(e) => setUfSelecionada(e.target.value)}
            >
              <option value="">Todos os Estados</option>
              <option value="SP">São Paulo (SP)</option>
              <option value="RJ">Rio de Janeiro (RJ)</option>
              <option value="MG">Minas Gerais (MG)</option>
              <option value="BA">Bahia (BA)</option>
              <option value="DF">Distrito Federal (DF)</option>
            </select>

            <select 
              className="p-2 rounded border border-slate-300 bg-white text-slate-700 flex-1 focus:outline-none focus:ring-2 focus:ring-blue-500 font-medium"
              value={ordemSelecionada}
              onChange={(e) => setOrdemSelecionada(e.target.value)}
            >
              <option value="">Ordenar de A a Z</option>
              <option value="menos_coerentes">Menos Coerentes Primeiro 🚨</option>
              <option value="mais_coerentes">Mais Coerentes Primeiro ✅</option>
            </select>
          </div>
        </div>

        <div className="overflow-x-auto">
          {carregando ? (
            <p className="text-center text-slate-500 py-8 animate-pulse">Buscando dados no servidor...</p>
          ) : (
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-slate-50 border-b border-slate-200 text-slate-600">
                  <th className="p-3 font-medium">Nome</th>
                  <th className="p-3 font-medium">Partido</th>
                  <th className="p-3 font-medium">UF</th>
                  <th className="p-3 font-medium">Cargo</th>
                  <th className="p-3 font-medium text-right">Score de Coerência</th>
                </tr>
              </thead>
              <tbody>
                {politicos.map((politico: any) => (
                  <tr 
                    key={politico.id} 
                    onClick={() => router.push(`/politico/${politico.id}`)}
                    className="border-b border-slate-100 hover:bg-slate-50 transition-colors cursor-pointer"
                  >
                    <td className="p-3 font-medium text-slate-800">{politico.nome_urna}</td>
                    <td className="p-3 text-slate-600">{politico.partido}</td>
                    <td className="p-3 text-slate-600">{politico.uf}</td>
                    <td className="p-3 text-slate-600">{politico.cargo}</td>
                    <td className="p-3 text-right">
                      <span className={`px-2 py-1 rounded text-sm font-semibold ${politico.score_coerencia > 70 ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                        {politico.score_coerencia}%
                      </span>
                    </td>
                  </tr>
                ))}
                
                {politicos.length === 0 && (
                  <tr>
                    <td colSpan={5} className="text-center p-8 text-slate-500">
                      Nenhum político encontrado com os filtros selecionados.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          )}
        </div>
      </main>

      {/* 4. RODAPÉ (FOOTER) */}
      <footer className="mt-16 border-t border-slate-200 pt-10 pb-6 text-slate-600">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8 max-w-6xl mx-auto">
          {/* Coluna 1: Marca e Info */}
          <div className="col-span-1 md:col-span-1">
            <h3 className="text-2xl font-bold text-slate-900 mb-3 tracking-tight">
              Contra<span className="text-emerald-600">Dito</span>
            </h3>
            <p className="text-sm text-slate-500 mb-4 leading-relaxed">
              Transparência política movida por Inteligência Artificial. Acompanhe a coerência de seus representantes.
            </p>
            <p className="text-xs text-slate-400 font-medium">
              © 2026 ContraDito.<br/>Squad 09 - UnB / FCTE.<br/>Licença MIT.
            </p>
          </div>

          {/* Coluna 2: Navegação */}
          <div>
            <h4 className="font-semibold text-slate-800 mb-4 uppercase text-xs tracking-widest">Navegação</h4>
            <ul className="space-y-3 text-sm">
              <li><a href="#" className="hover:text-emerald-600 transition-colors">Home</a></li>
              <li><a href="#" className="hover:text-emerald-600 transition-colors">Deputados</a></li>
              <li><a href="#" className="hover:text-emerald-600 transition-colors">Senadores</a></li>
            </ul>
          </div>

          {/* Coluna 3: Plataforma */}
          <div>
            <h4 className="font-semibold text-slate-800 mb-4 uppercase text-xs tracking-widest">Plataforma</h4>
            <ul className="space-y-3 text-sm">
              <li><a href="#" className="hover:text-emerald-600 transition-colors">Coerência</a></li>
              <li><a href="#" className="hover:text-emerald-600 transition-colors">Sobre o Projeto</a></li>
            </ul>
          </div>

          {/* Coluna 4: Projeto */}
          <div>
            <h4 className="font-semibold text-slate-800 mb-4 uppercase text-xs tracking-widest">Projeto</h4>
            <ul className="space-y-3 text-sm">
              <li><a href="https://github.com" target="_blank" className="hover:text-emerald-600 transition-colors">GitHub</a></li>
              <li><a href="#" className="hover:text-emerald-600 transition-colors">UnB - FCTE</a></li>
              <li><a href="#" className="hover:text-emerald-600 transition-colors">Squad 09 - MDS</a></li>
            </ul>
          </div>
        </div>

        {/* Linha fina no final com os créditos dos dados */}
        <div className="border-t border-slate-200 pt-6 text-center md:text-right max-w-6xl mx-auto">
          <p className="text-xs text-slate-400">
            Dados extraídos da API Aberta da Câmara dos Deputados e do Senado Federal. Modelos LLM utilizados para análise imparcial.
          </p>
        </div>
      </footer>

    </div>
  );
}