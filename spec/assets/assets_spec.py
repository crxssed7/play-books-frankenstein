# pyright: reportGeneralTypeIssues=false, reportFunctionMemberAccess=false

import os
from mamba import description, context, it, before, after
from expects import expect, equal
from unittest.mock import patch
import sys

from assets import image_base64, load_asset, load_asset_as_base64, resource_path

with description(resource_path) as self:
    with context("when sys._MEIPASS is set"):
        with before.each:
            self.patcher = patch.object(sys, "_MEIPASS", "/mocked/path", create=True)
            self.patcher.start()

        with after.each:
            self.patcher.stop()

        with it("returns the resource path with the _MEIPASS value"):
            path = resource_path("assets/img/img.png")
            expect(path).to(equal(f"/mocked/path/assets/img/img.png"))

    with context("when sys._MEIPASS is not set"):
        with before.each:
            self.patcher = patch.object(os.path, "abspath", return_value="/absolute/path")
            self.patcher.start()

        with after.each:
            self.patcher.stop()

        with it("returns the absolute path of the resource"):
            path = resource_path("assets/img/img.png")
            expect(path).to(equal(f"/absolute/path/assets/img/img.png"))

with description(load_asset):
    with before.each:
        current_path = os.path.abspath(".")
        self.patcher = patch.object(os.path, "abspath", return_value=os.path.join(current_path, "spec/support"))
        self.patcher.start()

    with after.each:
        self.patcher.stop()

    with it("returns the contents of the asset"):
        contents = load_asset("test.js")
        expect(contents).to(equal("console.log('Hello, World!');\n"))

with description(load_asset_as_base64):
    with before.each:
        current_path = os.path.abspath(".")
        self.patcher = patch.object(os.path, "abspath", return_value=os.path.join(current_path, "spec/support"))
        self.patcher.start()

    with after.each:
        self.patcher.stop()

    with it("returns the base64 contents of the asset"):
        contents = load_asset_as_base64("test.js")
        expect(contents).to(equal("Y29uc29sZS5sb2coJ0hlbGxvLCBXb3JsZCEnKTsK"))

with description(image_base64):
    with before.each:
        current_path = os.path.abspath(".")
        self.patcher = patch.object(os.path, "abspath", return_value=os.path.join(current_path, "spec/support"))
        self.patcher.start()

    with after.each:
        self.patcher.stop()

    with it("returns a base64 image url"):
        contents = image_base64("test.js")
        expect(contents).to(equal("data:image/png;base64,Y29uc29sZS5sb2coJ0hlbGxvLCBXb3JsZCEnKTsK"))
