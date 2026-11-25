create schema if not exists extensions;
create extension if not exists vector with schema extensions;

create schema if not exists cripto;

create table cripto.fragmentos (
    fuente text not null,
    posicion integer not null check (posicion >= 0),
    texto text not null check (length(trim(texto)) > 0),
    embedding extensions.vector(3072) not null,
    primary key (fuente, posicion)
);

create table cripto.conversaciones (
    id uuid primary key,
    propietario text not null,
    mensajes jsonb not null default '[]'::jsonb
        check (jsonb_typeof(mensajes) = 'array'),
    actualizada_en timestamptz not null default now()
);

create index conversaciones_propietario_actualizada_idx
    on cripto.conversaciones (propietario, actualizada_en desc);

alter table cripto.fragmentos enable row level security;
alter table cripto.conversaciones enable row level security;
