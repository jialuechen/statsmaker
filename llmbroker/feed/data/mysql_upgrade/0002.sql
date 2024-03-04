alter table `llmbroker_base`.`stocktypeinfo` modify column `minTradeNumber` double not null default 1;
alter table `llmbroker_base`.`stocktypeinfo` modify column `maxTradeNumber` double not null default 1;
UPDATE `llmbroker_base`.`version` set `version` = 2;
