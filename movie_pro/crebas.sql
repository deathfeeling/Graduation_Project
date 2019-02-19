drop table if exists tb_classification;

drop table if exists tb_comment;

drop table if exists tb_login_ip;

drop table if exists tb_movie;

drop table if exists tb_movie_classifications;

drop table if exists tb_region;

drop table if exists tb_user;

/*==============================================================*/
/* Table: tb_classification                                     */
/*==============================================================*/
create table tb_classification
(
   id_classification    integer not null auto_increment,
   classification       varchar(128),
   primary key (id_classification)
);

/*==============================================================*/
/* Table: tb_comment                                            */
/*==============================================================*/
create table tb_comment
(
   c_id                 integer not null auto_increment,
   comment              long varchar,
   id_user              integer,
   m_id                 integer,
   primary key (c_id)
);

/*==============================================================*/
/* Table: tb_login_ip                                           */
/*==============================================================*/
create table tb_login_ip
(
   id_ip                int not null auto_increment,
   ip_addr              varchar(128),
   login_date           datetime,
   u_id                 integer,
   primary key (id_ip)
);

/*==============================================================*/
/* Table: tb_movie                                              */
/*==============================================================*/
create table tb_movie
(
   m_id                 integer not null auto_increment,
   title                varchar(128),
   actor                varchar(1024),
   language             varchar(128),
   director             varchar(256),
   release_date         datetime,
   update_date          datetime,
   score                varchar(128),
   synopsis             long varchar,
   main_pic             varchar(256),
   pic                  varchar(1024),
   download_name        varchar(1024),
   download_size        varchar(128),
   download_thunder     varchar(4096),
   id_region            integer,
   primary key (m_id)
);

/*==============================================================*/
/* Table: tb_movie_classifications                              */
/*==============================================================*/
create table tb_movie_classifications
(
   id                   int not null auto_increment,
   m_id                 integer,
   id_classification    integer,
   primary key (id)
);

/*==============================================================*/
/* Table: tb_region                                             */
/*==============================================================*/
create table tb_region
(
   id_region            integer not null auto_increment,
   region               varchar(128),
   primary key (id_region)
);

/*==============================================================*/
/* Table: tb_user                                               */
/*==============================================================*/
create table tb_user
(
   u_id                 integer not null auto_increment,
   username             varchar(128),
   password             varchar(128),
   email                varchar(128),
   phone                varchar(128),
   register_date        datetime,
   register_ip          varchar(64),
   u_status             tinyint,
   primary key (u_id)
);

alter table tb_comment add constraint FK_Reference_1 foreign key (id_user)
      references tb_user (u_id) on delete restrict on update restrict;

alter table tb_comment add constraint FK_Reference_7 foreign key (m_id)
      references tb_movie (m_id) on delete restrict on update restrict;

alter table tb_login_ip add constraint FK_Reference_4 foreign key (u_id)
      references tb_user (u_id) on delete restrict on update restrict;

alter table tb_movie add constraint FK_Reference_3 foreign key (id_region)
      references tb_region (id_region) on delete restrict on update restrict;

alter table tb_movie_classifications add constraint FK_Reference_5 foreign key (m_id)
      references tb_movie (m_id) on delete restrict on update restrict;

alter table tb_movie_classifications add constraint FK_Reference_6 foreign key (id_classification)
      references tb_classification (id_classification) on delete restrict on update restrict;
