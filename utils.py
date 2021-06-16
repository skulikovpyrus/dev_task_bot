def get_initiator_approval_from_approvals(approvals, author):
    initiator = [approval for approval in approvals[1] if approval["person"]["id"] == author["id"]]
    if initiator:
        initiator = initiator[0]
        return initiator


def get_field_by_id(fields: list, _id: int):
    field = [field for field in fields if field["id"] == _id]
    if field:
        field = field[0]
        return field


def field_is_empty(field):
    return "value" not in field


def all_person_fields_are_empty(person_fields: list):
    return all(map(lambda x: field_is_empty(x), person_fields))


def person_has_approved(person_id, approvals, step):
    approval = [approval for approval in approvals[step - 1] if approval["person"]["id"] == person_id]
    if approval:
        approval = approval[0]
        return approval["approval_choice"] == "approved"


def person_participates_in_project(status_fields, status_field_id):
    field = [field for field in status_fields if field["id"] == status_field_id]
    if field:
        field = field[0]
        return field["value"]["choice_id"] != 1


def get_fields_to_lookup(status_fields):
    fields_to_lookup = []
    field_ids = list(status_to_person_relations.items())
    for status_id, person_id in field_ids:
        if person_participates_in_project(status_fields, status_id):
            fields_to_lookup.append(get_field_by_id(status_fields, person_id))
    return fields_to_lookup


# status_to_person_relations = {
#     23: 24,
#     26: 27,
#     31: 15,
#     33: 16,
#     35: 17,
#     37: 18,
#     47: 48,
#     41: 43
# }

status_to_person_relations = {
    6: 2,
    7: 8
}

participant_names = {
    2: "Дизайн",
    8: "Спека"
}

# participant_names = {
#     24: "Дизайн",
#     27: "Спека",
#     15: "Бэк",
#     16: "Фронт",
#     17: "iOS",
#     18: "Android",
#     48: "PyrusSync",
#     43: "Доки",
# }
