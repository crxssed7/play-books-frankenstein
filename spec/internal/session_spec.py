# pyright: reportGeneralTypeIssues=false, reportFunctionMemberAccess=false

from mamba import description, context, it
from expects import expect, equal

from internal.session import Session

with description(Session):
    with it("sets default variables to null-ish values"):
        session = Session()
        expect(session.active_hardcover_book).to(equal(None))
        expect(session.active_google_id).to(equal(None))
        expect(session.active_user_book_read).to(equal(None))
        expect(session.active_user_book_read_id).to(equal(None))
        expect(session.current_page).to(equal(0))
        expect(session.num_of_pages).to(equal(0))
        expect(session.percentage).to(equal(0))

    with description("start"):
        with it('sets the required variables'):
            session = Session()
            session.start({"book": "123"}, "12345", {"id": "123"}, 150)
            expect(session.active_hardcover_book).to(equal({"book": "123"}))
            expect(session.active_google_id).to(equal("12345"))
            expect(session.active_user_book_read).to(equal({"id": "123"}))
            expect(session.active_user_book_read_id).to(equal("123"))
            expect(session.num_of_pages).to(equal(150))

        with it('calculates the progress'):
            session = Session()
            session.percentage = 0.1 # 10%
            session.start({"book": "123"}, "12345", {"id": "123"}, 150)
            expect(session.current_page).to(equal(15))

    with description("stop"):
        with it("resets all variables"):
            session = Session()
            session.start({"book": "123"}, "12345", {"id": "123"}, 150)
            session.stop()
            expect(session.active_hardcover_book).to(equal(None))
            expect(session.active_google_id).to(equal(None))
            expect(session.active_user_book_read).to(equal(None))
            expect(session.active_user_book_read_id).to(equal(None))
            expect(session.current_page).to(equal(0))
            expect(session.num_of_pages).to(equal(0))
            expect(session.percentage).to(equal(0))

    with description("set_percentage"):
        with it("sets the percentage"):
            session = Session()
            session.set_percentage(0.4)
            expect(session.percentage).to(equal(0.4))

        with it("recalculates the progress"):
            session = Session()
            session.start({"book": "123"}, "12345", {"id": "123"}, 150)
            session.set_percentage(0.1)
            expect(session.current_page).to(equal(15))

    with description("is_active"):
        with context("when session is active"):
            with it("returns True"):
                session = Session()
                session.start({"book": "123"}, "12345", {"id": "123"}, 150)
                expect(session.is_active()).to(equal(True))

        with context("when session is not active"):
            with it("returns False"):
                session = Session()
                expect(session.is_active()).to(equal(False))
