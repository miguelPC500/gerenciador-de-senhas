const fs = require('fs');
const FILE_NAME = 'gerenciar.json';

const args = process.argv.slice(2);
const comando = args[0]; 

function lerBanco() {
    try {
        if (!fs.existsSync(FILE_NAME)) return [];
        return JSON.parse(fs.readFileSync(FILE_NAME, 'utf8'));
    } catch (err) {
        return [];
    }
}

function salvarBanco(lista) {
    fs.writeFileSync(FILE_NAME, JSON.stringify(lista, null, 2));
}

let lista = lerBanco();

if (comando === 'add') {
    const nome = args[1];
    const senha = args[2];
    if (nome && senha) {
        lista.push({ nome, senha });
        salvarBanco(lista);
    }
} else if (comando === 'delete') {
    const nomeRemover = args[1];
    const novaLista = lista.filter(item => item.nome !== nomeRemover);
    salvarBanco(novaLista);
}