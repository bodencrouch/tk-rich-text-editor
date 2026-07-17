"""Tkinter rich-text editor."""

__all__ = ["RichTextEditor"]


def __getattr__(name: str):
    if name == "RichTextEditor":
        from tk_rich_text_editor.rte_editor import RichTextEditor
        return RichTextEditor
    raise AttributeError(name)
