--
-- PostgreSQL database dump
--

-- Dumped from database version 12.5 (Ubuntu 12.5-1.pgdg18.04+1)
-- Dumped by pg_dump version 12.5 (Ubuntu 12.5-1.pgdg18.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: paymentType; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."paymentType" (id, name, value, is_available) FROM stdin;
1	cheap	CheapPaymentGateway	t
2	expensive	ExpensivePaymentGateway	t
3	premium	PremiumPaymentGateway	t
\.


--
-- Name: paymentType_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."paymentType_id_seq"', 3, true);


--
-- PostgreSQL database dump complete
--

