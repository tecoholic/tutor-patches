import warnings


from tutor_patches import Operation, PluginType, Slot


class TestSlot:
    def test_minimal_slot(self):
        slot = Slot(
            mfe="learner-dashboard",
            slot_name="course_list_slot",
            component="CustomCourseList",
        )
        assert slot.mfe == "learner-dashboard"
        assert slot.operation == Operation.INSERT
        assert slot.plugin_type == PluginType.DIRECT
        assert slot.priority == 50
        assert slot.hide_default is False

    def test_slot_with_all_options(self):
        slot = Slot(
            mfe="all",
            slot_name="footer_slot",
            component="CustomFooter",
            operation=Operation.HIDE,
            plugin_type=PluginType.IFRAME,
            priority=100,
            hide_default=True,
        )
        assert slot.mfe == "all"
        assert slot.operation == Operation.HIDE
        assert slot.plugin_type == PluginType.IFRAME
        assert slot.priority == 100

    def test_unknown_mfe_warns(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            Slot(
                mfe="unknown-mfe",
                slot_name="some_slot",
                component="SomeComponent",
            )
            assert len(w) == 1
            assert "Unknown MFE" in str(w[0].message)


class TestSlotJSX:
    def test_to_jsx_basic(self):
        slot = Slot(
            mfe="learner-dashboard",
            slot_name="course_list_slot",
            component="CustomCourseList",
        )
        jsx = slot.to_jsx()
        assert "PLUGIN_OPERATIONS.Insert" in jsx
        assert "DIRECT_PLUGIN" in jsx
        assert "priority: 50" in jsx
        assert "RenderWidget: CustomCourseList" in jsx
        assert "id: 'course_list_slot_CustomCourseList'" in jsx

    def test_to_hide_jsx(self):
        slot = Slot(
            mfe="all",
            slot_name="footer_slot",
            component="CustomFooter",
        )
        jsx = slot.to_hide_jsx()
        assert "PLUGIN_OPERATIONS.Hide" in jsx
        assert "default_contents" in jsx

    def test_to_tuples_without_hide(self):
        slot = Slot(
            mfe="learner-dashboard",
            slot_name="course_list_slot",
            component="CustomCourseList",
        )
        tuples = slot.to_tuples()
        assert len(tuples) == 1
        assert tuples[0][0] == "learner-dashboard"
        assert tuples[0][1] == "course_list_slot"

    def test_to_tuples_with_hide(self):
        slot = Slot(
            mfe="learner-dashboard",
            slot_name="course_list_slot",
            component="CustomCourseList",
            hide_default=True,
        )
        tuples = slot.to_tuples()
        assert len(tuples) == 2
        assert "Hide" in tuples[0][2]
        assert "Insert" in tuples[1][2]
