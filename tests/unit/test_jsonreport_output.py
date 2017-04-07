from nose.tools import assert_equals

from lettuce.plugins import jsonreport_output

META1 = {
    "features": {
        "total": 12,
        "success": 11,
        "failures": 1,
    },
    "scenarios": {
        "total": 24,
        "success": 22,
        "failures": 2,
    },
    "steps": {
        "total": 112,
        "success": 100,
        "failures": 2,
        "skipped": 5,
        "undefined": 5,
    },
    "is_success": False,
}
META2 = {
    "features": {
        "total": 1,
        "success": 1,
        "failures": 0,
    },
    "scenarios": {
        "total": 1,
        "success": 1,
        "failures": 0,
    },
    "steps": {
        "total": 1,
        "success": 1,
        "failures": 0,
        "skipped": 0,
        "undefined": 0,
    },
    "is_success": True,
}


def test__merge_meta():
    assert_equals(jsonreport_output._merge_meta(META1, META2), {
        "features": {
            "total": 13,
            "success": 12,
            "failures": 1,
        },
        "scenarios": {
            "total": 25,
            "success": 23,
            "failures": 2,
        },
        "steps": {
            "total": 113,
            "success": 101,
            "failures": 2,
            "skipped": 5,
            "undefined": 5,
        },
        "is_success": False,
    })


def test_merge_report_dicts_no_original():
    assert_equals(jsonreport_output.merge_report_dicts({"super": "dict"}, {}), {"super": "dict"})


def test_merge_report_dicts_does_the_job():
    report1 = {
        "meta": META1,
        "duration": 42,
        "features": ["feature1", "feature2"]
    }
    report2 = {
        "meta": META2,
        "duration": 1337,
        "features": ["feature3", "feature4"]
    }
    assert_equals(jsonreport_output.merge_report_dicts(report2, report1), {
        "duration": 1379,
        "features": ["feature1", "feature2", "feature3", "feature4"],
        "meta": {
            "features": {
                "total": 13,
                "success": 12,
                "failures": 1,
            },
            "scenarios": {
                "total": 25,
                "success": 23,
                "failures": 2,
            },
            "steps": {
                "total": 113,
                "success": 101,
                "failures": 2,
                "skipped": 5,
                "undefined": 5,
            },
            "is_success": False,
        },
    })
