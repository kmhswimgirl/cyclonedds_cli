class XMLFormatting:
    ''' A class to handle annoying XML formatting issues'''
    
    def _normalize_whitespace(elem):
        """Remove whitespace-only text/tail so indentation is applied consistently."""
        if elem.text is not None and elem.text.strip() == "":
            elem.text = None
        if elem.tail is not None and elem.tail.strip() == "":
            elem.tail = None
        for child in list(elem):
            XMLFormatting._normalize_whitespace(child)

    def _indent(elem, level=0):
        """
        Indent XML using tabs with consistent sibling tails.

        Each child's tail is set so all siblings start at the same indent level.
        Last child's tail aligns the parent's closing tag.
        """
        tab = "\t"
        nl = "\n"
        this_indent = nl + (tab * level)
        child_indent = nl + (tab * (level + 1))

        if len(elem):
            # set elem.text to newline + one deeper indent
            if elem.text is None or elem.text.strip() == "":
                elem.text = child_indent
            # recurse children and set their tails consistently
            for idx, child in enumerate(elem):
                XMLFormatting._indent(child, level + 1)
                if idx == len(elem) - 1:
                    # last child: tail aligns with parent's indentation
                    child.tail = this_indent
                else:
                    # non-last child: tail leaves place for next sibling at child indent
                    child.tail = child_indent
        else:
            # leaf node: give it a tail so following sibling lines up with parent
            if elem.tail is None or elem.tail.strip() == "":
                elem.tail = nl + (tab * level)
