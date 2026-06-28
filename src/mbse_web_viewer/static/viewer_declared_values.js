import { escapeHtml } from "./viewer_utils.js";


export function formatDeclaredValueHint(declaredValue) {
  if (declaredValue.type === "enum") {
    return declaredValue.type;
  }
  if (declaredValue.type === "bool") {
    return declaredValue.type;
  }
  return `${declaredValue.type} (${declaredValue.min}..${declaredValue.max})`;
}


export function renderDeclaredValueName(declaredValue, options = {}) {
  const inputId = options.inputId || `${declaredValue.name}-input`;
  const className = options.className || "declared-value-name";
  return `
    <label
      class="${escapeHtml(className)}"
      for="${escapeHtml(inputId)}"
      title="${escapeHtml(formatDeclaredValueHint(declaredValue))}"
    >
      ${escapeHtml(declaredValue.name)}
    </label>
  `;
}


export function renderDebuggerSummaryLine(label, value) {
  return [
    '<div class="debugger-queue-item">',
    `${escapeHtml(label)}: <strong>${escapeHtml(value)}</strong>`,
    "</div>",
  ].join("");
}


export function renderDeclaredValueInput(declaredValue, value, enums, options = {}) {
  const inputId = options.inputId || `${declaredValue.name}-input`;
  const inputName = options.inputName || "value";

  if (declaredValue.type === "bool") {
    return `
      <input
        id="${escapeHtml(inputId)}"
        name="${escapeHtml(inputName)}"
        type="checkbox"
        class="checkbox-input"
        ${value === true ? "checked" : ""}
      />
    `;
  }

  if (declaredValue.type === "enum") {
    const enumDefinition = getEnumById(declaredValue.enum_id, enums);
    const enumValues = enumDefinition?.values || [];
    return `
      <select id="${escapeHtml(inputId)}" name="${escapeHtml(inputName)}" required>
        <option value=""></option>
        ${enumValues
          .map((enumValue) => `
            <option value="${escapeHtml(enumValue)}" ${value === enumValue ? "selected" : ""}>
              ${escapeHtml(enumValue)}
            </option>
          `)
          .join("")}
      </select>
    `;
  }

  return `
    <input
      id="${escapeHtml(inputId)}"
      name="${escapeHtml(inputName)}"
      type="number"
      ${declaredValue.type === "float" ? 'step="any"' : 'step="1"'}
      min="${escapeHtml(String(declaredValue.min))}"
      max="${escapeHtml(String(declaredValue.max))}"
      required
      value="${value === undefined ? "" : escapeHtml(String(value))}"
    />
  `;
}


export function collectDeclaredValues(declaredValues, container) {
  const resolvedValues = {};

  for (const declaredValue of declaredValues) {
    const value = collectDeclaredValue(declaredValue, container);
    if (value === null) {
      return null;
    }
    resolvedValues[declaredValue.name] = value;
  }

  return resolvedValues;
}


export function collectDeclaredValue(declaredValue, container) {
  const input = container.querySelector(
    `[name="${declaredValue.name}"], [name="value"]`,
  );
  if (input === null) {
    return null;
  }

  if (declaredValue.type === "bool") {
    return Boolean(input.checked);
  }

  const rawValue = String(input.value || "").trim();
  if (rawValue.length === 0) {
    input.reportValidity?.();
    return null;
  }

  if (declaredValue.type === "enum") {
    return rawValue;
  }

  const numericValue = declaredValue.type === "float"
    ? Number.parseFloat(rawValue)
    : Number.parseInt(rawValue, 10);
  if (!Number.isFinite(numericValue)) {
    input.reportValidity?.();
    return null;
  }
  return numericValue;
}


export function isDeclaredValueInputDifferent(declaredValue, container, sessionValue) {
  const input = container.querySelector(
    `[name="${declaredValue.name}"], [name="value"]`,
  );
  if (input === null) {
    return false;
  }

  if (declaredValue.type === "bool") {
    return Boolean(input.checked) !== Boolean(sessionValue);
  }

  const rawValue = String(input.value || "").trim();
  if (declaredValue.type === "enum") {
    return rawValue !== String(sessionValue || "");
  }

  if (rawValue.length === 0) {
    return (
      sessionValue !== undefined
      && sessionValue !== null
      && String(sessionValue) !== ""
    );
  }

  const numericValue = declaredValue.type === "float"
    ? Number.parseFloat(rawValue)
    : Number.parseInt(rawValue, 10);
  if (!Number.isFinite(numericValue)) {
    return true;
  }
  return numericValue !== sessionValue;
}


function getEnumById(enumId, enums) {
  return enums.find((enumDefinition) => enumDefinition.id === enumId) || null;
}
