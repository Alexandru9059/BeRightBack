from brb.saving.models import SavingModel

class Saving(SavingModel):
    def converttodict(self) -> dict:
        d: dict = {
            "id": self.ID,
            "message": self.message,
            "cnt_commands": len(self.lastcommands),
            "last_commands": self.lastcommands,
        }

        return d