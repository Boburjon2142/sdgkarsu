document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll('textarea[name="body_uz"], textarea[name="body_en"]').forEach((source) => {
    let blocks;
    try {
      const documentData = JSON.parse(source.value);
      if (documentData.format === "sdg-news-blocks-v1" && Array.isArray(documentData.blocks)) blocks = documentData.blocks;
    } catch {}
    blocks = blocks || [{ type: "text", text: source.value }];
    const editor = document.createElement("div");
    editor.className = "news-block-editor";
    const list = document.createElement("div");
    list.className = "news-block-list";
    const toolbar = document.createElement("div");
    toolbar.className = "news-block-toolbar news-block-insert";
    const status = document.createElement("p");
    status.setAttribute("role", "status");
    const sync = () => {
      source.value = blocks.some(block => block.type === "table" || block.text.trim())
        ? JSON.stringify({ format: "sdg-news-blocks-v1", blocks }) : "";
    };
    const button = (label, action) => {
      const control = document.createElement("button");
      control.type = "button";
      control.textContent = label;
      control.addEventListener("click", action);
      return control;
    };
    const render = () => {
      list.replaceChildren();
      blocks.forEach((block, index) => {
        const panel = document.createElement("section");
        panel.className = "news-content-block";
        panel.classList.add(`news-content-block--${block.type}`);
        const controls = document.createElement("div");
        controls.className = "news-block-toolbar";
        const title = document.createElement("strong");
        title.textContent = `${index + 1}. ${block.type === "text" ? "Matn qismi" : "Jadval"}`;
        if (block.type === "table") {
          const dimensions = document.createElement("span");
          dimensions.className = "news-block-dimensions";
          dimensions.textContent = `${block.rows.length} × ${block.rows[0].length}`;
          title.append(dimensions);
        }
        controls.append(title);
        const move = (offset) => {
          [blocks[index], blocks[index + offset]] = [blocks[index + offset], blocks[index]];
          render();
        };
        const up = button("↑ Yuqoriga", () => move(-1));
        up.disabled = index === 0;
        const down = button("↓ Pastga", () => move(1));
        down.disabled = index === blocks.length - 1;
        controls.append(up, down, button("O'chirish", () => {
          const hasContent = block.type === "text" ? block.text.trim() : block.rows.some(row => row.some(cell => cell.trim()));
          if (hasContent && !window.confirm("Ushbu blok va undagi kontent o'chirilsinmi?")) return;
          blocks.splice(index, 1);
          render();
        }));
        panel.append(controls);
        if (block.type === "text") {
          const input = document.createElement("textarea");
          input.value = block.text;
          input.rows = 6;
          input.placeholder = "Yangilikning ushbu qismini shu yerga yozing…";
          input.setAttribute("aria-label", `${index + 1}. Matn qismi`);
          input.addEventListener("input", () => { block.text = input.value; sync(); });
          panel.append(input);
        } else {
          const scroll = document.createElement("div");
          scroll.className = "news-block-table-scroll";
          const table = document.createElement("table");
          block.rows.forEach((row, rowIndex) => {
            const tableRow = document.createElement("tr");
            row.forEach((cell, columnIndex) => {
              const tableCell = document.createElement(rowIndex === 0 ? "th" : "td");
              const input = document.createElement("textarea");
              input.rows = 2;
              input.value = cell;
              input.placeholder = rowIndex === 0 ? `Sarlavha ${columnIndex + 1}` : "Matn kiriting…";
              input.setAttribute("aria-label", `${index + 1}. Jadval, ${rowIndex + 1}-qator, ${columnIndex + 1}-ustun`);
              input.addEventListener("input", () => { block.rows[rowIndex][columnIndex] = input.value; sync(); });
              tableCell.append(input);
              tableRow.append(tableCell);
            });
            table.append(tableRow);
          });
          scroll.append(table);
          const hint = document.createElement("p");
          hint.textContent = "Birinchi qator — ustun sarlavhalari. Har bir katakka matn yozing.";
          panel.append(hint, scroll);
        }
        list.append(panel);
      });
      sync();
    };
    const add = (block) => {
      if (blocks.length >= 100) { status.textContent = "Eng ko'pi 100 ta blok qo'shish mumkin."; return; }
      blocks.push(block);
      render();
      list.lastElementChild.querySelector("textarea").focus();
    };
    const dimension = (label, defaultValue, maximum) => {
      const wrapper = document.createElement("label");
      wrapper.textContent = label;
      const input = document.createElement("input");
      input.type = "number";
      input.min = 1;
      input.max = maximum;
      input.value = defaultValue;
      wrapper.append(input);
      toolbar.append(wrapper);
      return input;
    };
    toolbar.append(button("+ Matn qismi", () => add({ type: "text", text: "" })));
    const rows = dimension("Qatorlar", 3, 50);
    const columns = dimension("Ustunlar", 3, 20);
    toolbar.append(button("+ Jadval chizish", () => {
      const rowCount = Number(rows.value);
      const columnCount = Number(columns.value);
      if (!Number.isInteger(rowCount) || rowCount < 1 || rowCount > 50 || !Number.isInteger(columnCount) || columnCount < 1 || columnCount > 20) {
        status.textContent = "Qatorlar: 1–50, ustunlar: 1–20 oralig'ida bo'lsin.";
        return;
      }
      status.textContent = "";
      add({ type: "table", rows: Array.from({ length: rowCount }, () => Array(columnCount).fill("")) });
    }));
    editor.append(list, toolbar, status);
    source.after(editor);
    render();
    source.hidden = true;
    source.form.addEventListener("submit", sync);
  });
});
