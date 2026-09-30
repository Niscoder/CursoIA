create table cliente (
	cpf varchar(11) primary key,
	nome varchar(100) not null,
	carteira numeric(10,2) not null default 0,
	email varchar(150) not null unique,
	
	check(carteira >= 0),
	check(CHAR_LENGTH(cpf) = 11)
);

create table cliente (
	cpf varchar(11) primary key,
	nome varchar(100) not null,
	carteira numeric(10,2) not null default 0,
	email varchar(150) not null unique,
	
	check(carteira >= 0),
	check(CHAR_LENGTH(cpf) = 11)
);


create table produto (
	id integer generated always as identity primary key,
	descricao varchar(150) not null,
	preco numeric(10,2) not null,
	
	check(preco > 0)
);

create table pedido (
	id integer generated always as identity primary key,
	cliente_cpf varchar(11) not null references cliente(cpf),
	produto_id integer not null references produto(id),
	qtd integer not null,
	
	check(qtd > 0)
);

insert into cliente (cpf, nome, email)
values ('55555555500', 'Andre', 'mail1@gmail.com'),
		('55555555501', 'Carlos', 'mail2@gmail.com'),
		('55555555502', 'Eduardo', 'mail3@gmail.com'),
		('55555555503', 'Felipe', 'mail4@gmail.com'),
		('55555555504', 'Guilherme', 'mail5@gmail.com'),
		('55555555505', 'Gustavo', 'mail6@gmail.com'),
		('55555555506', 'Murilo', 'mail7@gmail.com'),
		('55555555507', 'Miguel', 'mail8@gmail.com'),
		('55555555508', 'Maria', 'mail9@gmail.com'),
		('55555555509', 'Luiza', 'mail10@gmail.com'),
		('55555555510', 'José', 'mail11@gmail.com'),
		('55555555511', 'Luiz', 'mail12@gmail.com'),
		('55555555512', 'Gabriela', 'mai13@gmail.com'),
		('55555555513', 'Bruna', 'mail14@gmail.com'),
		('55555555514', 'Victor', 'mail15@gmail.com'),
		('55555555515', 'Vinicius', 'mail16@gmail.com');
