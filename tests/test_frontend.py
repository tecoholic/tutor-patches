from tutor_patches import FrontendPlugin, Slot


class TestFrontendPlugin:
    def test_minimal_plugin(self):
        plugin = FrontendPlugin(
            package="@myorg/frontend-plugin-foo",
            slots=[
                Slot(
                    mfe="learner-dashboard",
                    slot_name="course_list_slot",
                    component="CustomCourseList",
                ),
            ],
        )
        assert plugin.package == "@myorg/frontend-plugin-foo"
        assert len(plugin.slots) == 1
        assert plugin.local_path is None

    def test_plugin_with_local_path(self):
        plugin = FrontendPlugin(
            package="@myorg/frontend-plugin-foo",
            slots=[],
            local_path="/home/user/dev/frontend-plugin-foo",
        )
        assert plugin.local_path == "/home/user/dev/frontend-plugin-foo"


class TestFrontendPluginBuilders:
    def test_build_slot_tuples(self):
        plugin = FrontendPlugin(
            package="@myorg/frontend-plugin-foo",
            slots=[
                Slot(
                    mfe="learner-dashboard",
                    slot_name="course_list_slot",
                    component="CustomCourseList",
                ),
                Slot(
                    mfe="all",
                    slot_name="footer_slot",
                    component="CustomFooter",
                    hide_default=True,
                ),
            ],
        )
        tuples = plugin._build_slot_tuples()
        assert len(tuples) == 3  # 1 + 2 (one with hide_default)

    def test_build_import_statement(self):
        plugin = FrontendPlugin(
            package="@myorg/frontend-plugin-foo",
            slots=[
                Slot(
                    mfe="learner-dashboard",
                    slot_name="course_list_slot",
                    component="CustomCourseList",
                ),
                Slot(
                    mfe="all",
                    slot_name="footer_slot",
                    component="CustomFooter",
                ),
            ],
        )
        import_stmt = plugin._build_import_statement()
        assert import_stmt == "import { CustomCourseList, CustomFooter } from '@myorg/frontend-plugin-foo';"

    def test_build_import_statement_deduplicates(self):
        plugin = FrontendPlugin(
            package="@myorg/frontend-plugin-foo",
            slots=[
                Slot(mfe="learner-dashboard", slot_name="slot1", component="Foo"),
                Slot(mfe="profile", slot_name="slot2", component="Foo"),
            ],
        )
        import_stmt = plugin._build_import_statement()
        assert import_stmt == "import { Foo } from '@myorg/frontend-plugin-foo';"

    def test_build_npm_install(self):
        plugin = FrontendPlugin(
            package="@myorg/frontend-plugin-foo",
            slots=[],
        )
        npm_cmd = plugin._build_npm_install()
        assert npm_cmd == "RUN npm install @myorg/frontend-plugin-foo"
