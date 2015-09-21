import logging
from crypt_keeper.entry import Entry
from fnmatch import fnmatch


log = logging.getLogger(__name__)


def ext_pillar_exec(minion_id, pillar, *args, **kwargs):
    log.info("Fetching crypt data for minion %s", minion_id)
    pillar_data = {}

    for key in Entry.keys():
        log.debug("Fetching crypt key %s", key)
        entry = Entry(key=key)

        if "__minions__" in entry.value.keys():
            log.debug("Performing __minions__ check for key %s on minion %s", key, minion_id)
            minions = entry.value["__minions__"]
            if True not in [fnmatch(minion_id, match) for match in minions.split(',')]:
                log.debug("__minions__ data does not match minion %s: %s", minion_id, minions)
                continue
            else:
                log.debug("__minions__ data matches minion %s: %s", minion_id, minions)
                del entry.value["__minions__"]

        data_part = pillar_data
        for key_part in key.split(":"):
            data_part.setdefault(key_part, {})
            data_part = data_part[key_part]

        for key, val in entry.value.iteritems():
            data_part[key] = val

    log.debug("Finalized crypt pillar data for minion %s: %s", minion_id, pillar_data)
    return {"crypt": pillar_data}
