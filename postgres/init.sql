ALTER USER delivery_user WITH REPLICATION SUPERUSER;

CREATE SCHEMA shipment;
CREATE TABLE public.return_scan_log (
    id integer NOT NULL,
    distance_from_hub double precision NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    shipment_id integer NOT NULL,
    driver_id integer NOT NULL,
    subco_id integer NOT NULL
);

CREATE SEQUENCE public.return_scan_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.return_scan_log OWNER TO delivery_user;

ALTER TABLE ONLY public.return_scan_log
    ADD CONSTRAINT return_scan_log_pk PRIMARY KEY (id);

    
CREATE TABLE shipment.shipment_features (
    id integer NOT NULL,
    shipment_id integer NOT NULL,
    require_proof_of_delivery boolean DEFAULT false NOT NULL,
    no_signature boolean DEFAULT false NOT NULL,
    no_neighbour_delivery boolean DEFAULT false NOT NULL,
    deliver_in_mail_box boolean DEFAULT false NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    require_age_check boolean DEFAULT false,
    require_otp boolean DEFAULT false,
    uses_sms_feature boolean DEFAULT false NOT NULL,
    has_branded_track_trace boolean DEFAULT false
);

CREATE SEQUENCE shipment.shipment_features_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE shipment.shipment_features OWNER TO delivery_user;

ALTER TABLE ONLY shipment.shipment_features
    ADD CONSTRAINT shipment_features_pk PRIMARY KEY (id);