# Alura inator 3000
Baixador de cursos da Alura

## AVISO
Não me responsabilizo pelo que você faz com o script nem com os vídeos que baixar.

## Como usar:
Instale as packages com `pip install -r ./requirements.txt`

Insira seu login e sua senha em credentials conforme o exemplo abaixo:

```py
credentials = {
	'username': 'username@email.com',
	'password': 'Password123'
}
```

Insira o link do curso que você deseja baixar em `baseUrl` conforme os exemplos abaixo:

```py
baseUrl = 'https://cursos.alura.com.br/course/introducao-a-programacao-com-ruby-e-jogos-1'
```

```py
baseUrl = 'https://cursos.alura.com.br/course/introducao-a-programacao-com-c-parte-3'
```

```py
baseUrl = 'https://cursos.alura.com.br/course/python-pygame-pacman-colisao-pontuacao'
```

Rode o script com `python ./main.py` e espere todos os vídeos serem baixados.
