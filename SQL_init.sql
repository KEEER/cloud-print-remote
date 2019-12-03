CREATE TABLE public.cp_sessions
(
    kiuid uuid NOT NULL,
    jobs varchar(4)[],
    debt bigint,
    CONSTRAINT cp_sessions_pkey PRIMARY KEY (kiuid)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

CREATE TABLE public.print_codes
(
    code character varying(4) COLLATE pg_catalog."default" NOT NULL,
    kiuid uuid NOT NULL,
    CONSTRAINT print_codes_pkey PRIMARY KEY (code)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;