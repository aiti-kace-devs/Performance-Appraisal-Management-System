import { DatePipe } from '@angular/common';
export const MOBILE_WIDTH_BREAKPOINT = 600;
export const TABLET_WIDTH_BREAKPOINT = 960;
export const DEFAULT_PAGE_SIZE = 50;

export const APP_REFRESH_TOKEN = 'appriasal-app-refresh-token';
export const APP_ACCESS_TOKEN = 'appriasal-app-access-token';
export const USER_INFO = 'appriasal-app-user';

export enum PrimeNgSeverity {
  Info = 'info',
  Danger = 'danger',
  Success = 'success',
  Warn = 'warn',
  Custom = 'custom',
  Error = 'error',
}

export const enum PrimeNgAlerts {
  SUCCESS = 'Success',
  INFO = 'Info',
  ERROR = 'Error',
  WARNING = 'Warn',
  UNOBSTRUSIVE = 'Unobstrusive',
}

export const TOAST_TIME = 3000;
export enum DialogPosition {
  LEFT = 'left',
  RIGHT = 'right',
  TOP_RIGHT = 'top-right',
  TOP_LEFT = 'top-left',
  TOP = 'top',
  BOTTOM_LEFT = 'bottom-left',
  BOTTOM_RIGHT = 'bottom-right',
  BOTTOM = 'bottom',
  CENTER = 'center',
}

export const GenericErrorMessage =
  'Sorry, an error occurred. Rest assured, it will be fixed';

export const trackById = (
  index: number,
  data: { [key: string]: any }
): number => {
  return data['id'];
};

export const ERROR_MESSAGES_MAPPING = {
  errors: {
    useValue: {
      required: 'This field is required',
      minlength: ({ requiredLength, actualLength }: any) =>
        `Please enter ${requiredLength} or more characters. Current count: ${actualLength}`,
      maxlength: ({ requiredLength, actualLength }: any) =>
        `Please enter  ${requiredLength} or less characters. Current count: ${actualLength}`,
      email: () => `Please enter a valid email`,
      mismatch: () => `Passwords do not match`,
      validatePhoneNumber: 'Invalid phone number supplied.',
      min: ({ actual, min }: any) =>
        `${actual} isn't a valid choice. The lowest value should be ${min}.`,
      max: ({ actual, max }: any) =>
        `${actual} isn't a valid choice. The highest value should be ${max}.`,
      emailExists: () => 'Email address already registered. Try another',
    },
  },
};

export const blurPrdicateFunction = (element: Element) =>
  [
    'INPUT',
    'P-AUTOCOMPLETE',
    'TEXTAREA',
    'SELECT',
    'P-DROPDOWN',
    'P-CALENDAR',
    'P-PASSWORD',
    'P-NUMBER',
    'P-CHECKBOX',
    'P-MULTISELECT',
    'P-CHIPS',
    'NGX-INTL-TEL-INPUT',
    'P-INPUTNUMBER',
    'P-EDITOR',
    'P-FILEUPLOAD',
  ].some((selector) => element.tagName === selector);

export const anchorErrorComponentFn = (
  hostElement: Element,
  errorElement: Element
) => {
  let errorNode: Element | null | undefined = hostElement?.querySelector(
    'custom-control-error'
  );

  const isInputGroup =
    hostElement?.parentElement?.classList.contains('p-inputgroup');

  if (isInputGroup) {
    hostElement?.parentElement?.insertAdjacentElement('afterend', errorElement);
    errorNode = hostElement?.parentElement?.querySelector(
      'custom-control-error'
    );
  } else {
    hostElement?.insertAdjacentElement('afterend', errorElement);
  }

  return () => {
    if (errorNode) {
      errorNode.remove();
    }
  };
};

export const ISODate = (date = new Date()) => {
  const dateString = date.toISOString();
  return dateString.split('T')[0];
};

export const ISOTime = (date = new Date(), resetSeconds = true) => {
  if (resetSeconds) {
    date.setSeconds(0);
  }
  const dateString = date.toISOString();
  return dateString.split('T')[1].split('.')[0];
};
