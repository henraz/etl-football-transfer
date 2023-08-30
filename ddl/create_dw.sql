CREATE TABLE `project-dev.dw-football-transfer.dim_club` (
                id_club INTEGER NOT NULL,
                club_name STRING
);


CREATE TABLE `project-dev.dw-football-transfer.dim_player` (
                id_player INTEGER NOT NULL,
                player_name STRING,
                age INTEGER,
                position INTEGER
);


CREATE TABLE `project-dev.dw-football-transfer.dim_league` (
                id_league INTEGER NOT NULL,
                league_name STRING
);


CREATE TABLE `project-dev.dw-football-transfer.dim_transfer` (
                id_transfer INTEGER NOT NULL,
                transfer_movement STRING
);


CREATE TABLE `project-dev.dw-football-transfer.dim_club_involv` (
                id_club_involv INTEGER NOT NULL,
                club_involved_name STRING
);


CREATE TABLE `project-dev.dw-football-transfer.dim_country` (
                id_country INTEGER NOT NULL,
                country_name STRING
);


CREATE TABLE `project-dev.dw-football-transfer.dim_date_season` (
                id_time INTEGER NOT NULL,
                year_transf INTEGER,
                season STRING,
                transfer_period STRING
);


CREATE TABLE `project-dev.dw-football-transfer.fact_transfer` (
                id_club INTEGER NOT NULL,
                id_player INTEGER NOT NULL,
                id_league INTEGER NOT NULL,
                id_time INTEGER NOT NULL,
                id_country INTEGER NOT NULL,
                id_transfer INTEGER NOT NULL,
                id_club_involv INTEGER NOT NULL,
                fee NUMERIC(12,2),
                fee_description STRING
);