alter table cripto.fragmentos
    add column pagina integer check (pagina > 0),
    add column modelo_embedding text;
