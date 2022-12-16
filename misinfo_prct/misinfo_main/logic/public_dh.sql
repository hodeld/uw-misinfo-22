CREATE TABLE public.abstract (
    corpusid int primary key,
    abstract text,
    updated timestamp with time zone not null
);


CREATE TABLE public.authors (
    authorid bigint primary key,
    url text,
    name text,
    aliases text[],
    affiliations text,
    homepage text,
    papercount int,
    citationcount int,
    hindex int,
    updated timestamp with time zone not null
);

CREATE TABLE public.citations (
    citingcorpusid int,
    citedcorpusid int,
    isinfluential boolean,
    contexts text[],
    intents text[],
    updated timestamp with time zone not null
);

/* authors and access info in separate tables */
CREATE TABLE public.papers (
    corpusid int primary key,
    title text,
    referencecount int,
    citationcount int,
    influentialcitationcount int,
    isopenaccess boolean,
    venue text,
    s2fieldsofstudy text[],
    publicationtypes text[],
    publicationdate date,
    paperyear int,
    updated timestamp with time zone not null
);

CREATE TABLE public.author2paper (
    corpusid int not null,
    authorid bigint,
    name text
);

CREATE TABLE public.papers_openaccessinfo (
    corpusid int primary key,
    ACL text,
    DBLP text,
    Arxiv text,
    MAG text,
    PubMed text,
    DOI text,
    PubMedCentral text,
    license text,
    status text,
    url text
);

/* "text" is in the content dictionary: content["text"] */
/* "source" is in the content dictionary: content["source"] */
CREATE TABLE public.s2orc (
    corpusid int primary key,
    source text,
    text text,
    annotations text,
    updated timestamp with time zone not null
);


CREATE TABLE public.paper-ids (
    corpusid int primary key,
    sha text,
);

CREATE TABLE public.embeddings (
    corpusid int primary key,
    model text,
    vector text,
);


CREATE TABLE public.tldrs (
    corpusid int primary key,
    model text,
    text text,
);


