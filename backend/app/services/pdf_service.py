from app.parsers.bank_parser import BankStatementParser


class PDFService:

    @staticmethod
    def parse_statement(filepath: str):

        return BankStatementParser.parse(filepath)