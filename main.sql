PRAGMA foreign_keys = ON;
DROP TABLE host;
DROP TABLE ansible_child_group;
DROP TABLE ansible_parent_group;
DROP TABLE ansible_access_group;


CREATE TABLE ansible_parent_group(
   id INTEGER PRIMARY KEY,
   group_name TEXT,
   descr TEXT,
   vendor TEXT
);

INSERT INTO ansible_parent_group (group_name,descr,vendor)
VALUES
    ("SMGR","System Manager","Avaya"),
    ("SM","Session Manager","Avaya"),
    ("CM","Communication Manager","Avaya"),
    ("ADS","Avaya Diagnostic Server","Avaya"),
    ("AADS","Avaya Aura Device Services","Avaya"),
    ("AAM","Avaya Aura Messaging","Avaya"),
    ("AAMS","Avaya Aura Media Server","Avaya"),
    ("AAWG","Avaya Aura Web Gateway","Avaya"),
    ("AES","Application Enablement Services","Avaya"),
    ("AEM","Avaya Equinox Management","Avaya"),
    ("AEMS","Avaya Equinox Media Server","Avaya"),
    ("AEP","Avaya Experience Portal","Avaya"),
    ("AMM","Avaya Multimedia Messaging","Avaya"),
    ("ASP","Avaya Solutions Platform","Avaya"),
    ("AVP","Avaya Virtualization Platform","Avaya"),
    ("AVPU","AVP Utilities","Avaya"),
    ("BREEZE","Breeze","Avaya"),
    ("ESXI","ESXI Host","VMware"),
    ("SBCE","Session Border Controller for Enterprise","Avaya");


CREATE TABLE ansible_child_group(
   id INTEGER PRIMARY KEY,
   group_name TEXT,
   descr TEXT,
   parent_group_id INTEGER NOT NULL,
   FOREIGN KEY (parent_group_id)
      REFERENCES ansible_parent_group(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);

INSERT INTO ansible_child_group (group_name,descr,parent_group_id)
VALUES
    ("smgrpri","Primary System Manager",1),
    ("smgrgeo","Geo System Manager",1),
    ("asm","Core Session Manager",2),
    ("bsm","Branch Session Manager",2),
    ("cmmain","Main Communication Manager",3),
    ("cmess","ESS Communication Manager",3),
    ("cmlsp","LSP Communication Manager",3);

CREATE TABLE ansible_access_group(
   id INTEGER NOT NULL PRIMARY KEY,
   group_name TEXT NOT NULL,
   ansible_user TEXT NOT NULL,
   ansible_password TEXT NOT NULL,
   ansible_become_user TEXT DEFAULT "root",
   ansible_become_pass TEXT,
   ansible_become_method TEXT DEFAULT "su",
   ansible_connection TEXT DEFAULT "ssh",
   ansible_port INTEGER DEFAULT 22,
   ssh_args TEXT
);

INSERT INTO ansible_access_group (group_name,ansible_user,ansible_password,ansible_become_pass)
VALUES
    ("Core CMs","combat","cmb@Dm1n","cmb@Dm1n"),
    ("Core SMs","combat","cmb@Dm1n","cmb@Dm1n");


CREATE TABLE host(
   id INTEGER NOT NULL PRIMARY KEY,
   inventory_hostname TEXT NOT NULL UNIQUE,
   ansible_host TEXT NOT NULL,
   ansible_parent_group_id TEXT NOT NULL,
   ansible_child_group_id TEXT,
   ansible_access_group_id INTEGER,
   ansible_user TEXT,
   ansible_password TEXT,
   ansible_become_user TEXT DEFAULT "root",
   ansible_become_pass TEXT,
   ansible_become_method TEXT DEFAULT "su",
   ansible_connection TEXT DEFAULT "ssh",
   ansible_port INTEGER DEFAULT 22,
   ssh_args TEXT,
   FOREIGN KEY (ansible_parent_group_id)
      REFERENCES ansible_parent_group(id)
      ON UPDATE CASCADE
      ON DELETE RESTRICT
   FOREIGN KEY (ansible_child_group_id)
      REFERENCES ansible_child_group(id)
      ON UPDATE CASCADE
      ON DELETE SET NULL
   FOREIGN KEY (ansible_access_group_id)
      REFERENCES ansible_access_group(id)
      ON UPDATE CASCADE
      ON DELETE SET NULL
);

INSERT INTO host (inventory_hostname,ansible_host,ansible_parent_group_id,ansible_child_group_id,ansible_user,ansible_password,ansible_become_pass)
VALUES
    ("smgr","192.168.11.101",1,1,"combat","cmb@Dm1n","cmb@Dm1n"),
    ("sm","192.168.11.102",2,3,"combat","cmb@Dm1n","cmb@Dm1n");

-- DROP TABLE ansible_parent_group;
-- DELETE FROM ansible_parent_group;
-- SELECT * from ansible_parent_group;
-- DROP TABLE ansible_child_group;
-- DELETE FROM ansible_child_group;
-- SELECT * from ansible_child_group;
-- DROP TABLE host;
-- DELETE FROM host;
-- SELECT * from host;
-- DROP TABLE ansible_access_group;
-- DELETE FROM ansible_access_group;
-- SELECT * from ansible_access_group;