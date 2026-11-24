# GitHub Branch Protection Configuration

## 🔒 Configuración de Branch Protection Rules

### 📋 Checklist completo

```
✅ Branch: main (production)
✅ Branch: develop (integration)
✅ CI/CD workflow configurado
✅ Secrets configurados
```

---

## 🎯 Paso a Paso

### 1️⃣ Ir a Settings

**URL directa:** https://github.com/1AdrianM/job-fit-ai/settings/branches

O manualmente:
1. Ve al repo: https://github.com/1AdrianM/job-fit-ai
2. Click en **"Settings"** (tab arriba)
3. Click en **"Branches"** (menú izquierda)

---

### 2️⃣ Proteger `main` (Producción)

Click: **"Add branch protection rule"**

#### **Branch name pattern:**
```
main
```

#### **Configuración recomendada:**

**✅ Protect matching branches:**

- [x] **Require a pull request before merging**
  - [x] Require approvals: **1**
  - [x] Dismiss stale pull request approvals when new commits are pushed
  - [ ] Require review from Code Owners (opcional, si usas CODEOWNERS)

- [x] **Require status checks to pass before merging**
  - [x] Require branches to be up to date before merging
  - **Status checks required** (seleccionar después de primer CI run):
    - `test` (Run Tests)
    - `lint` (Code Quality)

- [x] **Require conversation resolution before merging**

- [ ] **Require signed commits** (opcional, para mayor seguridad)

- [ ] **Require linear history** (opcional, si prefieres rebase)

- [x] **Require deployments to succeed before merging** (opcional, si configuras environments)

**✅ Rules applied to everyone including administrators:**

- [x] **Do not allow bypassing the above settings**

**✅ Restrict pushes:**

- [x] **Restrict who can push to matching branches** (opcional)
  - Solo tú o colaboradores específicos

**❌ Allow force pushes:**

- [ ] **NO** (mantener desmarcado)

**❌ Allow deletions:**

- [ ] **NO** (mantener desmarcado)

**📌 Click:** "Create" o "Save changes"

---

### 3️⃣ Proteger `develop` (Integración)

Click: **"Add rule"** (nueva regla)

#### **Branch name pattern:**
```
develop
```

#### **Configuración recomendada:**

**✅ Protect matching branches:**

- [x] **Require a pull request before merging**
  - [x] Require approvals: **0** (si trabajas solo) o **1** (en equipo)
  - [ ] Dismiss stale pull request approvals (opcional para develop)

- [x] **Require status checks to pass before merging**
  - [x] Require branches to be up to date before merging
  - **Status checks required:**
    - `test` (Run Tests)
    - `lint` (Code Quality)

- [x] **Require conversation resolution before merging**

- [ ] **Require signed commits** (opcional)

**✅ Rules applied to everyone:**

- [ ] **Do not allow bypassing** (opcional, menos estricto que main)

**❌ Allow force pushes:**

- [ ] **NO**

**❌ Allow deletions:**

- [ ] **NO**

**📌 Click:** "Create"

---

## 🤖 Status Checks

### ⚠️ Nota importante:

Los status checks (`test` y `lint`) **solo aparecerán** después de que el CI/CD workflow corra por primera vez.

**Para que aparezcan:**

1. Crea el workflow `.github/workflows/ci.yml` (instrucciones abajo)
2. Pushea a `develop` o crea un PR
3. Espera que el workflow termine
4. Vuelve a Settings → Branches → Edit rule
5. En "Status checks", busca `test` y `lint` y selecciónalos

---

## 📊 Resultado final

Cuando todo esté configurado, verás:

```
Branch protection rules

main
  ✓ Require pull request
  ✓ Require status checks
  ✓ Require conversation resolution
  ✓ Do not allow bypassing
  ✓ Restrict force pushes
  ✓ Restrict deletions

develop
  ✓ Require pull request
  ✓ Require status checks
  ✓ Restrict force pushes
  ✓ Restrict deletions
```

---

## 🔄 Workflow después de configurar

### Para cualquier cambio:

```bash
# 1. No puedes pushear directamente a main o develop
git push origin main  # ❌ RECHAZADO

# 2. Debes crear un branch y un PR
git checkout -b feature/my-change
git push origin feature/my-change

# 3. Crear PR en GitHub
# El CI corre automáticamente

# 4. Si CI pasa ✅ → puedes mergear
# 5. Si CI falla ❌ → arreglar y pushear de nuevo
```

---

## 🎯 Verificación

Para verificar que funciona:

1. **Intenta pushear a main:**
   ```bash
   git checkout main
   echo "test" >> README.md
   git commit -am "test"
   git push origin main
   ```
   
   **Resultado esperado:** ❌ Rechazado con mensaje:
   ```
   ! [remote rejected] main -> main (protected branch hook declined)
   ```

2. **Crea un PR y verifica que el CI corra**

3. **Intenta mergear sin que pasen los checks** → Debe estar bloqueado

---

## 📚 Recursos

- [GitHub Branch Protection Docs](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [Required Status Checks](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches#require-status-checks-before-merging)

---

## 🆘 Troubleshooting

**❓ No veo los status checks (test, lint) para seleccionar**

→ El CI no ha corrido todavía. Crea el workflow primero y espera que corra.

**❓ Quiero hacer cambios de emergencia en main**

→ Si eres admin, puedes temporalmente deshabilitar la protección, pero NO es recomendado. Mejor usa un hotfix branch.

**❓ El PR dice "Review required" pero soy el único contributor**

→ Puedes aprobar tu propio PR o reducir el número de approvals requeridos a 0.

---

**✅ Con esto tendrás Git Flow profesional configurado en GitHub!**
