# pyright: reportGeneralTypeIssues=false, reportFunctionMemberAccess=false

import os
from mamba import description, context, it, before, after
from expects import expect, equal
from unittest.mock import patch

from internal.matches import Matches

with description(Matches) as self:
    with it("loads matches from json file"):
        matches_file = os.path.join(os.path.abspath("."), "spec/support/assets/matches_readonly.json")
        with patch("internal.matches.MATCHES_FILE", matches_file):
            matches = Matches()
            expected = {
                "ZJKSOQAAAXXX": {
                    "title": "The Wild Robot",
                    "id": 150193,
                    "pages": 288,
                    "editions": [{ "id": 31658065, "title": "The Wild Robot" }]
                }
            }
            expect(matches.matches).to(equal(expected))

    with description("save_match"):
        with before.each:
            self.matches_file = os.path.join(os.path.abspath("."), "spec/support/assets/matches.json")
            self.patcher = patch("internal.matches.MATCHES_FILE", self.matches_file)
            self.patcher.start()

        with after.each:
            os.remove(self.matches_file)
            self.patcher.stop()

        with it("saves the match to a dict"):
            matches = Matches()
            matches.save_match("ZJKSOQAAAXXX", {
                "title": "The Wild Robot",
                "id": 150193,
                "pages": 288,
                "editions": [{ "id": 31658065, "title": "The Wild Robot" }]
            })
            expect(matches.matches).to(equal({
                "ZJKSOQAAAXXX": {
                    "title": "The Wild Robot",
                    "id": 150193,
                    "pages": 288,
                    "editions": [{ "id": 31658065, "title": "The Wild Robot" }]
                }
            }))

        with it("saves the match to json file"):
            matches = Matches()
            matches.save_match("ZJKSOQAAAXXX", {
                "title": "The Wild Robot",
                "id": 150193,
                "pages": 288,
                "editions": [{ "id": 31658065, "title": "The Wild Robot" }]
            })
            with open(self.matches_file, "r") as f:
                matches = Matches()
                expect(matches.matches).to(equal({
                    "ZJKSOQAAAXXX": {
                        "title": "The Wild Robot",
                        "id": 150193,
                        "pages": 288,
                        "editions": [{ "id": 31658065, "title": "The Wild Robot" }]
                    }
                }))

    with description("get"):
        with context("when match exists"):
            with it("returns the match"):
                matches_file = os.path.join(os.path.abspath("."), "spec/support/assets/matches_readonly.json")
                with patch("internal.matches.MATCHES_FILE", matches_file):
                    matches = Matches()
                    expected = {
                        "title": "The Wild Robot",
                        "id": 150193,
                        "pages": 288,
                        "editions": [{ "id": 31658065, "title": "The Wild Robot" }]
                    }
                    expect(matches.get("ZJKSOQAAAXXX")).to(equal(expected))

        with context("when match does not exist"):
            with it("returns None"):
                matches_file = os.path.join(os.path.abspath("."), "spec/support/assets/matches_readonly.json")
                with patch("internal.matches.MATCHES_FILE", matches_file):
                    matches = Matches()
                    expect(matches.get("NONEXISTANT")).to(equal(None))
