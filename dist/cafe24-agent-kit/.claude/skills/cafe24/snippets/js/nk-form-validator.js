/*!
 * nk-form-validator — 폼 유효성 검사 (이메일·전화·필수 입력, 에러 메시지 표시)
 * 사용처: 로그인·회원가입·문의·주문서 등 모든 입력 폼
 * 의존성: nk-form-controls.css (에러 클래스 .nk-field.is-error 활용)
 *
 * 비코더 사용법:
 *   1. SFTP로 _nk/js/ 폴더에 업로드
 *   2. layout.html 의 </body> 직전에 <script src="/_nk/js/nk-form-validator.js" defer></script>
 *   3. HTML 구조 (nk-form-controls.css 패턴):
 *      <form data-nk-validate>
 *        <div class="nk-field">
 *          <label class="nk-label" for="email">이메일</label>
 *          <input class="nk-input" id="email" name="email" type="email" required>
 *          <p class="nk-field-error" data-nk-error-for="email"></p>
 *        </div>
 *        <div class="nk-field">
 *          <label class="nk-label" for="phone">전화번호</label>
 *          <input class="nk-input" id="phone" name="phone" type="tel" data-nk-rule="phone-kr" required>
 *          <p class="nk-field-error" data-nk-error-for="phone"></p>
 *        </div>
 *        <button type="submit" class="nk-btn nk-btn-primary">제출</button>
 *      </form>
 *
 *   4. 지원 규칙 (HTML 속성으로 지정):
 *      - required: HTML5 required 속성
 *      - type="email": 이메일 형식
 *      - type="tel" + data-nk-rule="phone-kr": 한국 전화번호 (010-1234-5678)
 *      - minlength / maxlength: HTML5 표준
 *      - data-nk-rule="password": 8자 이상 + 영문/숫자/특수문자 중 2종
 *      - data-nk-rule="business-no": 사업자등록번호 (000-00-00000)
 *      - data-nk-rule="match:OTHER_NAME": 다른 input 값과 동일 (비밀번호 확인용)
 *
 *   5. 에러 메시지는 자동 한국어 표시. 직접 지정하려면:
 *      <input data-nk-message-required="아이디를 입력해주세요">
 */

(function () {
  'use strict';

  const DEFAULT_MESSAGES = {
    required: '필수 입력 항목입니다.',
    email: '올바른 이메일 형식이 아닙니다.',
    tel: '올바른 전화번호 형식이 아닙니다.',
    'phone-kr': '010-0000-0000 형식으로 입력해주세요.',
    'business-no': '000-00-00000 형식으로 입력해주세요.',
    password: '8자 이상, 영문·숫자·특수문자 중 2가지를 조합해주세요.',
    minlength: (n) => `최소 ${n}자 이상 입력해주세요.`,
    maxlength: (n) => `최대 ${n}자까지 입력 가능합니다.`,
    match: (name) => `${name} 항목과 일치하지 않습니다.`,
  };

  const PATTERNS = {
    email: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
    'phone-kr': /^01[016789]-?\d{3,4}-?\d{4}$/,
    'business-no': /^\d{3}-?\d{2}-?\d{5}$/,
  };

  function getMessage(input, rule, param) {
    const custom = input.dataset['nkMessage' + rule.charAt(0).toUpperCase() + rule.slice(1)];
    if (custom) return custom;
    const def = DEFAULT_MESSAGES[rule];
    return typeof def === 'function' ? def(param) : def;
  }

  function showError(input, message) {
    const field = input.closest('.nk-field');
    if (!field) return;
    field.classList.add('is-error');
    input.setAttribute('aria-invalid', 'true');

    const errorEl =
      field.querySelector(`[data-nk-error-for="${input.id}"]`) ||
      field.querySelector('.nk-field-error');
    if (errorEl) errorEl.textContent = message;
  }

  function clearError(input) {
    const field = input.closest('.nk-field');
    if (!field) return;
    field.classList.remove('is-error');
    input.removeAttribute('aria-invalid');

    const errorEl =
      field.querySelector(`[data-nk-error-for="${input.id}"]`) ||
      field.querySelector('.nk-field-error');
    if (errorEl) errorEl.textContent = '';
  }

  function validateInput(input) {
    const value = (input.value || '').trim();

    // 1. required
    if (input.required && !value) {
      showError(input, getMessage(input, 'required'));
      return false;
    }

    // 빈 값 + required 아님 → 통과
    if (!value) {
      clearError(input);
      return true;
    }

    // 2. type=email
    if (input.type === 'email' && !PATTERNS.email.test(value)) {
      showError(input, getMessage(input, 'email'));
      return false;
    }

    // 3. minlength / maxlength
    if (input.minLength > 0 && value.length < input.minLength) {
      showError(input, getMessage(input, 'minlength', input.minLength));
      return false;
    }
    if (input.maxLength > 0 && value.length > input.maxLength) {
      showError(input, getMessage(input, 'maxlength', input.maxLength));
      return false;
    }

    // 4. data-nk-rule
    const rule = input.dataset.nkRule;
    if (rule) {
      // match:other
      if (rule.startsWith('match:')) {
        const otherName = rule.slice(6);
        const other = input.form && input.form.elements[otherName];
        if (other && value !== other.value) {
          const otherLabel = other.closest('.nk-field')?.querySelector('.nk-label')?.textContent || otherName;
          showError(input, getMessage(input, 'match', otherLabel));
          return false;
        }
      }
      // 정규식 룰
      else if (PATTERNS[rule] && !PATTERNS[rule].test(value)) {
        showError(input, getMessage(input, rule));
        return false;
      }
      // password
      else if (rule === 'password') {
        const hasAlpha = /[a-zA-Z]/.test(value);
        const hasDigit = /\d/.test(value);
        const hasSpec = /[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\\/;'`~]/.test(value);
        const types = [hasAlpha, hasDigit, hasSpec].filter(Boolean).length;
        if (value.length < 8 || types < 2) {
          showError(input, getMessage(input, 'password'));
          return false;
        }
      }
    }

    clearError(input);
    return true;
  }

  function validateForm(form) {
    const inputs = form.querySelectorAll('input, textarea, select');
    let firstInvalid = null;
    let valid = true;
    inputs.forEach((input) => {
      // hidden, submit, button 건너뛰기
      if (['hidden', 'submit', 'button', 'reset'].includes(input.type)) return;
      if (!validateInput(input) && !firstInvalid) {
        firstInvalid = input;
        valid = false;
      } else if (!validateInput(input)) {
        valid = false;
      }
    });
    if (firstInvalid) {
      firstInvalid.focus();
      firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
    return valid;
  }

  // 모든 data-nk-validate 폼에 적용
  document.querySelectorAll('form[data-nk-validate]').forEach((form) => {
    // 제출 시 검증
    form.addEventListener('submit', (e) => {
      if (!validateForm(form)) {
        e.preventDefault();
      }
    });

    // 입력 시 실시간 검증 (blur 후 입력)
    form.addEventListener('input', (e) => {
      const input = e.target;
      if (!input.matches('input, textarea, select')) return;
      // 이미 에러 상태일 때만 실시간 재검증 (UX: 처음부터 에러 표시 X)
      const field = input.closest('.nk-field');
      if (field && field.classList.contains('is-error')) {
        validateInput(input);
      }
    });

    // 블러 시 검증
    form.addEventListener(
      'blur',
      (e) => {
        const input = e.target;
        if (input.matches('input, textarea, select')) {
          validateInput(input);
        }
      },
      true
    );
  });

  // 전역 API
  window.nkForm = {
    validate: validateForm,
    validateInput: validateInput,
    clearError: clearError,
  };
})();
