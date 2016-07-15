import json

from lettuce.terrain import after


def enable(filename=None):
    filename = filename or "lettucetests.json"

    @after.all
    def generate_json_output(total):
        """
        This callback is called after all the features are
        ran.
        """
        total_dict = total_result_to_dict(total)
        with open(filename, "w") as handle:
            json.dump(total_dict, handle)


def total_result_to_dict(total):
    """
    Transform a `TotalResult` to a json-serializable Python dictionary.

    :param total:               a `TotalResult` instance
    :return:                    a Python dictionary
    """
    return {
        "meta": extract_meta(total),
        "features": [
            extract_feature_data(feature_result)
            for feature_result in total.feature_results
        ]
    }


def extract_feature_data(feature_result):
    """
    Extract data from a `FeatureResult` instance.

    :param feature_result:                a `FeatureResult` instance
    :return:                              a Python dictionary
    """
    scenarios = []
    meta = {
        "total": 0,
        "success": 0,
        "failures": 0,
        "skipped": 0,
        "undefined": 0
    }
    for scenario_result in feature_result.scenario_results:
        scenario_data = extract_scenario_data(scenario_result)
        scenarios.append(scenario_data)
        meta["total"] += scenario_data["meta"]["total"]
        meta["success"] += scenario_data["meta"]["success"]
        meta["failures"] += scenario_data["meta"]["failures"]
        meta["skipped"] += scenario_data["meta"]["skipped"]
        meta["undefined"] += scenario_data["meta"]["undefined"]

    return {
        "name": feature_result.feature.name,
        "meta": meta,
        "scenarios": scenarios
    }


def extract_scenario_data(scenario_result):
    """
    Extract data from a `ScenarioResult` instance.

    :param scenario_result:              a `ScenarioResult` instance
    :return:                             a Python dictionary
    """
    return {
        "name": scenario_result.scenario.name,
        "outline": scenario_result.outline,
        "meta": {
            "total": scenario_result.total_steps,
            "success": len(scenario_result.steps_passed),
            "failures": len(scenario_result.steps_failed),
            "skipped": len(scenario_result.steps_skipped),
            "undefined": len(scenario_result.steps_undefined),
        },
        "steps": [extract_step_data(step) for step in scenario_result.all_steps]
    }


def extract_step_data(step):
    """
    Extract data from a `Step` instance.

    :param step:                         a `Step` instance
    :return                              a Python dictionary
    """
    step_data = {
        "name": step.sentence,
        "meta": {
            "success": step.passed,
            "failed": step.failed,
            "skipped": not step.passed and not step.failed and step.has_definition,
            "undefined": not step.has_definition,
        },
        "failure": {}
    }
    if step.why:
        step_data["failure"] = {
            "exception": repr(step.why.exception),
            "traceback": step.why.traceback
        }
    return step_data


def extract_meta(total):
    """
    Extract metadata from the `TotalResult`.

    :param total:               a `TotalResult` instance
    :return:                    a Python dictionary
    """
    return {
        "features": {
            "total": total.features_ran,
            "success": total.features_passed,
            "failures": total.features_ran - total.features_passed,
        },
        "scenarios": {
            "total": total.scenarios_ran,
            "success": total.scenarios_passed,
            "failures": total.scenarios_ran - total.scenarios_passed,
        },
        "steps": {
            "total": total.steps,
            "success": total.steps_passed,
            "failures": total.steps_failed,
            "skipped": total.steps_skipped,
            "undefined": total.steps_undefined,
        },
        "is_success": total.is_success,
    }
