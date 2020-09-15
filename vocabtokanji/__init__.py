# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo
# import all of the Qt GUI library
from aqt.qt import *


class DeckDialog(QDialog):
    """
    Class for the dialog box to choose decks and note fields, has to be in a class so that the functions that update
    the dropdown boxes can access the text chosen in the other dropdown boxes.
    """
    def __init__(self, parent, my_config):
        super().__init__(parent)

        # Get the names of all the decks
        deck_names_list = []
        for a_deck in mw.col.decks.all_names_and_ids():
            deck_names_list.append(a_deck.name)

        # Build textbox
        self.setWindowModality(Qt.WindowModal)
        self.l = QGridLayout()
        self.setLayout(self.l)
        self.l.setColumnMinimumWidth(0, 200)
        self.l.setColumnMinimumWidth(1, 200)
        self.tv1 = QLabel("Vocabulary deck")
        self.l.addWidget(self.tv1, 0, 1)
        self.tv2 = QLabel("Kanji deck")
        self.l.addWidget(self.tv2, 0, 0)
        self.th1 = QLabel("Word field")
        self.l.addWidget(self.th1, 2, 1)
        self.th2 = QLabel("Kanji field")
        self.l.addWidget(self.th2, 2, 0)
        self.tr = QLabel("Kanji radicals/components field")
        self.l.addWidget(self.tr, 4, 0)
        self.cdeck1 = QComboBox()
        self.cdeck1.addItem("-")
        self.cdeck1.addItems(deck_names_list)
        self.l.addWidget(self.cdeck1, 1, 1)
        self.cdeck2 = QComboBox()
        self.cdeck2.addItem("-")
        self.cdeck2.addItems(deck_names_list)
        self.l.addWidget(self.cdeck2, 1, 0)
        self.cfield1 = QComboBox()
        self.l.addWidget(self.cfield1, 3, 1)
        self.cfield2 = QComboBox()
        self.l.addWidget(self.cfield2, 3, 0)
        self.ccompo = QComboBox()
        self.l.addWidget(self.ccompo, 5, 0)

        # Set the current text in the comboboxes to what we had in memory in the configuration (if we had something)
        if my_config:
            self.cdeck1.setCurrentText(my_config["vocab_deck"])
            self.cdeck2.setCurrentText(my_config["kanji_deck"])
            self.update_fields_dropdown1()
            self.update_fields_dropdown2()
            self.update_fields_dropdown3()
            self.cfield1.setCurrentText(my_config["vocab_field"])
            self.cfield2.setCurrentText(my_config["kanji_field"])
            self.ccompo.setCurrentText(my_config["components_field"])

        # Connect signals
        self.cdeck1.currentTextChanged.connect(self.update_fields_dropdown1)
        self.cdeck2.currentTextChanged.connect(self.update_fields_dropdown2)
        self.cdeck2.currentTextChanged.connect(self.update_fields_dropdown3)

        # Add Ok and Cancel buttons
        self.bb = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.bb.accepted.connect(self.accept)
        self.bb.rejected.connect(self.reject)
        self.l.addWidget(self.bb, 6, 0, 1, -1)

    def update_fields_dropdown1(self):
        """
        Updates the "Word field" dropdown box according to choice made in the "Vocabulary deck" dropdown box.
        """
        cards_from_deck = mw.col.find_cards(r'"deck:' + self.cdeck1.currentText() + r'"')

        for a_card_id in cards_from_deck:
            a_card = mw.col.getCard(a_card_id)
            break
        if 'a_card' in locals():
            a_note = a_card.note()
            self.cfield1.clear()
            self.ccompo.addItem("-")
            self.cfield1.addItems(a_note.keys())
        else:
            self.cfield1.clear()
            self.cfield1.addItems(["-"])

    def update_fields_dropdown2(self):
        """
        Updates the "Kanji field" dropdown box according to choice made in the "Kanji deck" dropdown box.
        """
        cards_from_deck = mw.col.find_cards(r'"deck:' + self.cdeck2.currentText() + r'"')

        for a_card_id in cards_from_deck:
            a_card = mw.col.getCard(a_card_id)
            break
        if 'a_card' in locals():
            a_note = a_card.note()
            self.cfield2.clear()
            self.ccompo.addItem("-")
            self.cfield2.addItems(a_note.keys())
        else:
            self.cfield2.clear()
            self.cfield2.addItem("-")

    def update_fields_dropdown3(self):
        """
        Updates the "Components field" dropdown box according to choice made in the "Kanji deck" dropdown box.
        """
        cards_from_deck = mw.col.find_cards(r'"deck:' + self.cdeck2.currentText() + r'"')

        for a_card_id in cards_from_deck:
            a_card = mw.col.getCard(a_card_id)
            break
        if 'a_card' in locals():
            a_note = a_card.note()
            self.ccompo.clear()
            self.ccompo.addItem("-")
            self.ccompo.addItems(a_note.keys())
            self.ccompo.setCurrentIndex(2)
        else:
            self.ccompo.clear()
            self.ccompo.addItem("-")



def set_decks():
    """
    Checks if the configuration has fields for this addon, if not, adds them.

    Opens a dialog box so that the user can select the correct decks and fields.

    Saves the names of the chosen decks and fields to the configuration
    """

    # Put the saved configuration to show in the dialog box
    try:
        my_config ={
            "vocab_deck":       mw.col.conf.get_immutable("kanji_unlock_addon_vocab_deck"),
            "kanji_deck":       mw.col.conf.get_immutable("kanji_unlock_addon_kanji_deck"),
            "vocab_field":      mw.col.conf.get_immutable("kanji_unlock_addon_vocab_field"),
            "kanji_field":      mw.col.conf.get_immutable("kanji_unlock_addon_kanji_field"),
            "components_field": mw.col.conf.get_immutable("kanji_unlock_addon_components_field")
            }
    except:
        my_config = {}

    parent = mw.app.activeWindow()
    d = DeckDialog(parent, my_config)

    if d.exec_():
        # Check if all decks and fields are not "-" (except radical/component field)
        if d.cdeck1.currentText() == "-" or d.cdeck2.currentText() == "-" or \
                d.cfield1.currentText() == "-" or d.cfield2.currentText() == "-":
            showInfo("Please select a value for all decks and fields. (Kanji radicals/components field is optional "
                     "but recommended.)")
        # Check that both selected decks are not the same
        elif d.cdeck1.currentText() == d.cdeck2.currentText():
            showInfo("The kanji deck and the vocabulary deck must be different decks.")
        else:
            # The selected names are saved to the configuration
            mw.col.conf.set("kanji_unlock_addon_vocab_deck", d.cdeck1.currentText())
            mw.col.conf.set("kanji_unlock_addon_kanji_deck", d.cdeck2.currentText())
            mw.col.conf.set("kanji_unlock_addon_vocab_field", d.cfield1.currentText())
            mw.col.conf.set("kanji_unlock_addon_kanji_field", d.cfield2.currentText())
            mw.col.conf.set("kanji_unlock_addon_components_field", d.ccompo.currentText())
        return 0
    else:
        # "Cancel" was pressed
        return -1


def validate_configuration(my_config):
    """
    First checks if mw.col.conf contains all the needed deck names and field names, if it doesn't, tells the user to
    set the kanji/vocabulary decks and exits.

    Checks if the set kanji/vocab decks/fields are valid, if they aren't, we tell the user and exit.

    If no kanji cards are suspended, tells the user to go suspend the kanji in the card browser.

    Otherwise all is well.
    """

    # Get the names of the decks
    deck_names_list = []
    for a_deck in mw.col.decks.all_names_and_ids():
        deck_names_list.append(a_deck.name)
    # Check if saved deck names are present in Anki
    if my_config["vocab_deck"] not in deck_names_list:
        showInfo(r'Deck "%s" cannot be found' % my_config["vocab_deck"])
        return False
    if my_config["kanji_deck"] not in deck_names_list:
        showInfo(r'Deck "%s" cannot be found' % my_config["kanji_deck"])
        return False

    # Get the field names in those decks
    cards_from_vocab_deck = mw.col.find_cards(r'"deck:' + my_config["vocab_deck"] + r'"')
    cards_from_kanji_deck = mw.col.find_cards(r'"deck:' + my_config["kanji_deck"] + r'"')

    for a_card_id in cards_from_vocab_deck:
        a_card = mw.col.getCard(a_card_id)
        break
    if 'a_card' not in locals():
        showInfo(r'Cannot find cards in deck"%s"' % my_config["vocab_deck"])
        return False
    else:
        a_note = a_card.note()
        vocab_fields = a_note.keys()

    for a_card_id in cards_from_kanji_deck:
        a_card = mw.col.getCard(a_card_id)
        break
    if 'a_card' not in locals():
        showInfo(r'Cannot find cards in deck"%s"' % my_config["kanji_deck"])
        return False
    else:
        a_note = a_card.note()
        kanji_fields = a_note.keys()

    if my_config["vocab_field"] not in vocab_fields:
        showInfo(r'Cannot find field "%s" in deck "%s".' % (my_config["vocab_field"], my_config["vocab_deck"]))
        return False
    if my_config["kanji_field"] not in kanji_fields:
        showInfo(r'Cannot find field "%s" in deck "%s".' % (my_config["kanji_field"], my_config["kanji_deck"]))
        return False
    if my_config["components_field"] != "-" and my_config["components_field"] not in kanji_fields:
        showInfo(r'Cannot find field "%s" in deck "%s".' % (my_config["components_field"], my_config["kanji_deck"]))
        return False

    # Check if there are suspended cards in the Kanji deck
    cards_from_kanji_deck = mw.col.find_cards(r'"deck:' + my_config["kanji_deck"] + r'" is:suspended')
    if not cards_from_kanji_deck:
        showInfo(r'There are no suspended kanji cards in "%s". This script works on kanji cards that are suspended. '
                 r'Suspend cards in the Anki card browser.' % my_config["kanji_deck"])
        return False

    # All's right with the world
    return True


def unsuspend_kanji():
    """
    Load the saved configuration.

    Get the new vocabulary cards, get the notes for those cards.

    For each new vocabulary note, get the kanji contained in that word

    For each kanji collected, check if it has kanji cards that are suspended.

    After user confirmation, unsuspend the new kanji cards, add the tag "kanjiunsuspended" on the new vocabulary notes.
    """

    # Regex for kanji search in fields
    import re

    # Check if saved configuration exists
    try:
        my_config = {
            "vocab_deck": mw.col.conf.get_immutable("kanji_unlock_addon_vocab_deck"),
            "kanji_deck": mw.col.conf.get_immutable("kanji_unlock_addon_kanji_deck"),
            "vocab_field": mw.col.conf.get_immutable("kanji_unlock_addon_vocab_field"),
            "kanji_field": mw.col.conf.get_immutable("kanji_unlock_addon_kanji_field"),
            "components_field": mw.col.conf.get_immutable("kanji_unlock_addon_components_field")
        }
    except:
        showInfo("Please set the vocabulary and kanji decks with\nTools > KanjiUnlockAddon: Set vocabulary/kanji decks")
    else:
        # Configuration exists, check if it is valid
        if validate_configuration(my_config) is True:

            # Kanji and radicals regular expression unicode block
            # https://github.com/olsgaard/Japanese_nlp_scripts/blob/master/jp_regex.py
            kanji_chars = r'[⺀-⿕㐀-䶵一-鿋豈-頻]'
            # \d+[⺀-⿕㐀-䶵一-鿋豈-頻]\r\n\d+[⺀-⿕㐀-䶵一-鿋豈-頻]\r\n

            # Create a dialog window
            parent = mw.app.activeWindow()
            d = QDialog(parent)
            d.setWindowModality(Qt.WindowModal)
            d.l = QGridLayout()
            d.setLayout(d.l)
            d.l.setColumnMinimumWidth(0, 120)
            d.l.setRowMinimumHeight(1, 100)
            d.l.setRowMinimumHeight(3, 100)

            d.tb1 = QTextEdit()
            d.tb1.setReadOnly(True)
            d.tb1.setFontPointSize(12)
            d.l.addWidget(d.tb1, 1, 0)
            d.tb2 = QTextEdit()
            d.tb2.setReadOnly(True)
            d.tb2.setFontPointSize(12)
            d.l.addWidget(d.tb2, 3, 0)
            d.bb = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
            d.bb.accepted.connect(d.accept)
            d.bb.rejected.connect(d.reject)
            d.l.addWidget(d.bb, 4, 0, 1, -1)

            big_kanji_list = []  # new and old kanji from new vocab words
            card_ids_to_unsuspend = []
            note_ids_reviewing = set()

            # Get the new cards, the cards that are in review but haven't yet been tagged with "kanjiunsuspended"
            # "deck:Core 2000" is:review -tag:kanjiunsuspended
            card_ids_reviewing = mw.col.find_cards(r'"deck:' + my_config["vocab_deck"] + r'" is:review '
                                                   r'-tag:kanjiunsuspended')

            # for each of those cards
            for card_id in card_ids_reviewing:
                # get the note (if not have already)
                note_ids_reviewing.add(mw.col.getCard(card_id).nid)

            # We now have a list of all new notes in review
            # for each note
            for note_id in note_ids_reviewing:
                a_note = mw.col.getNote(note_id)
                # get the actual word
                actual_word = a_note[my_config["vocab_field"]]
                # Put it in the text box
                d.tb1.append(actual_word)
                kanji_in_word = re.findall(kanji_chars, actual_word)
                for a_kanji in kanji_in_word:
                    add_to_kanji_list(a_kanji, big_kanji_list, my_config, kanji_chars)

            # Done collecting all of the kanji from the new cards, time to find which of them have yet to be unsuspended
            for a_kanji in big_kanji_list:
                # get cards with that kanji (from appropriate field) that are suspended
                # example "deck:All in one Kanji - RTK order (new edition)" "Kanji:指" -is:suspended
                card_ids = mw.col.findCards(r'"deck:' + my_config["kanji_deck"] + r'" "' + my_config["kanji_field"] +
                                            r':' + a_kanji + r'" is:suspended')
                if card_ids:
                    # Put kanji in text box
                    d.tb2.append(a_kanji)
                    # add cards to card_ids_to_unsuspend
                    card_ids_to_unsuspend.extend(card_ids)

            # Add labels with the total number of new words and new kanji
            d.t1 = QLabel("New words: %d" % len(note_ids_reviewing))
            d.l.addWidget(d.t1, 0, 0)
            d.t2 = QLabel("New Kanji: %d (new cards: %d)" % (len(re.findall(kanji_chars, d.tb2.toPlainText())),
                                                             len(card_ids_to_unsuspend)))
            d.l.addWidget(d.t2, 2, 0)

            '''
            # for debug purposes
            d.tb1.clear()
            for a_card_id in card_ids_to_unsuspend:
                a_card = mw.col.getCard(a_card_id)
                a_note = mw.col.getNote(a_card.nid)
                d.tb1.append(str(a_card_id) + a_note["Kanji"])
            '''

            # Ask for user confirmation
            if d.exec_():
                # add the tag kanjiunsuspended to all cards in big_word_id_list
                for a_note_id in note_ids_reviewing:
                    a_note = mw.col.getNote(a_note_id)
                    a_note.addTag("kanjiunsuspended")
                    a_note.flush()

                # Unsuspend new kanji
                if card_ids_to_unsuspend:
                    mw.col.sched.unsuspendCards(card_ids_to_unsuspend)
                # Refresh main window
                mw.reset()
                return 0
            else:
                return -1


def add_to_kanji_list(a_kanji, big_kanji_list, my_config, kanji_chars):
    """
    Add a_kanji to big_kanji_list if not already in it.
    If the kanji note has a "components" field with other kanji in it, calls itself for those kanji has well.
    """

    import re  # Should be already imported from unsuspend_kanji

    if a_kanji not in big_kanji_list:
        big_kanji_list.append(a_kanji)

        if my_config["components_field"] != "-":
            # Get the a card for that kanji like "deck:All in one Kanji - RTK order (new edition)" "Kanji:指"
            card_ids_for_kanji = mw.col.findCards(r'"deck:' + my_config["kanji_deck"] + r'" "' +
                                                  my_config["kanji_field"] + ":" + a_kanji + r'"')
            for a_card_id in card_ids_for_kanji:
                a_card = mw.col.getCard(a_card_id)
                a_note = a_card.note()
                components = a_note[my_config["components_field"]]
                components = re.findall(kanji_chars, components)  # Simplify to just kanji characters
                for a_component in components:
                    add_to_kanji_list(a_component, big_kanji_list, my_config, kanji_chars)
                break  # break because we don't need more than one card


def clear_saved_conf():
    mw.col.conf.remove("kanji_unlock_addon_vocab_deck")
    mw.col.conf.remove("kanji_unlock_addon_kanji_deck")
    mw.col.conf.remove("kanji_unlock_addon_vocab_field")
    mw.col.conf.remove("kanji_unlock_addon_kanji_field")
    mw.col.conf.remove("kanji_unlock_addon_components_field")


# create 2 new menu items, "KanjiUnlockAddon: Unsuspend new kanji" and "KanjiUnlockAddon: Set vocabulary/kanji decks"
actionUnsuspend = QAction("KanjiUnlockAddon: Unsuspend new kanji", mw)
actionSetDecks = QAction("KanjiUnlockAddon: Set vocabulary/kanji decks", mw)
# actionRemoveConf = QAction("DEBUG Remove conf", mw)  # for debug purposes

# set them to call function when clicked
actionUnsuspend.triggered.connect(unsuspend_kanji)
actionSetDecks.triggered.connect(set_decks)
# actionRemoveConf.triggered.connect(clear_saved_conf)

# and add it to the tools menu
mw.form.menuTools.addAction(actionUnsuspend)
mw.form.menuTools.addAction(actionSetDecks)
# mw.form.menuTools.addAction(actionRemoveConf)
