/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { ListRenderer } from "@web/views/list/list_renderer";

function _getAdjacentRecord(list, record, delta) {
    const records = list.records;
    let index = records.indexOf(record) + delta;
    if (index < 0) {
        index = records.length - 1;
    } else if (index >= records.length) {
        index = 0;
    }
    return records[index];
}

patch(ListRenderer.prototype, {
    onCellKeydownReadOnlyMode(hotkey, cell, group, record) {
        if (hotkey === "f2" && record) {
            const column = this.columns.find(c => c.name === cell.getAttribute("name"));
            this.cellToFocus = { column, record };
            this.props.list.enterEditMode(record);
            return true;
        }
        return super.onCellKeydownReadOnlyMode(...arguments);
    },

    onCellKeydownEditMode(hotkey, cell, group, record) {
        const result = (() => {
            const { list } = this.props;
            const row = cell.parentElement;
            if (hotkey === "arrowleft") {
                const toFocus = this.findPreviousFocusableOnRow(row, cell);
                if (toFocus) {
                    this.focus(toFocus);
                    return true;
                }
            } else if (hotkey === "arrowright") {
                const toFocus = this.findNextFocusableOnRow(row, cell);
                if (toFocus) {
                    this.focus(toFocus);
                    return true;
                }
            } else if (hotkey === "arrowup" || hotkey === "arrowdown") {
                const delta = hotkey === "arrowup" ? -1 : 1;
                const futureRecord = _getAdjacentRecord(list, record, delta);
                list.leaveEditMode({ validate: true }).then((canProceed) => {
                    if (canProceed) {
                        list.enterEditMode(futureRecord);
                    }
                });
                return true;
            }
            return false;
        })();
        if (result) {
            return true;
        }
        return super.onCellKeydownEditMode(...arguments);
    },
});
