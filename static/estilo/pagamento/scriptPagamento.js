// Alternar entre métodos de pagamento
document.addEventListener('DOMContentLoaded', function () {
    const paymentOptions = document.querySelectorAll('.payment-option');
    const cardForm = document.getElementById('card-form');

    paymentOptions.forEach(option => {
        option.addEventListener('click', function () {
            // Remove seleção anterior
            paymentOptions.forEach(opt => opt.classList.remove('selected'));

            // Marca opção clicada
            this.classList.add('selected');

            // Mostra ou esconde o formulário do cartão
            cardForm.style.display = (this.id === 'credit-card-option') ? 'block' : 'none';
        });
    });
});



// // ==========================
// // Integração Mercado Pago
// // ==========================
//
// const cardNumberElement = mp.fields.create('cardNumber', {
//     placeholder: "Número do cartão"
// }).mount('form-checkout__cardNumber');
//
// const expirationDateElement = mp.fields.create('expirationDate', {
//     placeholder: "MM/AA"
// }).mount('form-checkout__expirationDate');
//
// const securityCodeElement = mp.fields.create('securityCode', {
//     placeholder: "Código de segurança"
// }).mount('form-checkout__securityCode');
//
// // Busca tipos de identificação
// (async function getIdentificationTypes() {
//     try {
//         const identificationTypes = await mp.getIdentificationTypes();
//         const identificationTypeElement = document.getElementById('form-checkout__identificationType');
//         createSelectOptions(identificationTypeElement, identificationTypes);
//     } catch (e) {
//         console.error('Erro ao obter tipos de identificação:', e);
//     }
// })();
//
// // Cria opções para <select>
// function createSelectOptions(elem, options, labelsAndKeys = { label: "name", value: "id" }) {
//     const { label, value } = labelsAndKeys;
//     elem.innerHTML = "";
//
//     const fragment = document.createDocumentFragment();
//     options.forEach(option => {
//         const opt = document.createElement('option');
//         opt.value = option[value];
//         opt.textContent = option[label];
//         fragment.appendChild(opt);
//     });
//
//     elem.appendChild(fragment);
// }
//
// const paymentMethodElement = document.getElementById('paymentMethodId');
// const issuerElement = document.getElementById('form-checkout__issuer');
// const installmentsElement = document.getElementById('form-checkout__installments');
//
// const issuerPlaceholder = "Banco emissor";
// const installmentsPlaceholder = "Parcelas";
//
// let currentBin;
//
// // Detecta mudanças no número do cartão
// cardNumberElement.on('binChange', async ({ bin }) => {
//     try {
//         if (!bin && paymentMethodElement.value) {
//             clearSelectsAndSetPlaceholders();
//             paymentMethodElement.value = "";
//             return;
//         }
//
//         if (bin && bin !== currentBin) {
//             const { results } = await mp.getPaymentMethods({ bin });
//             const paymentMethod = results[0];
//             paymentMethodElement.value = paymentMethod.id;
//
//             updatePCIFieldsSettings(paymentMethod);
//             await updateIssuer(paymentMethod, bin);
//             await updateInstallments(paymentMethod, bin);
//         }
//
//         currentBin = bin;
//     } catch (e) {
//         console.error('Erro ao obter método de pagamento:', e);
//     }
// });
//
// function clearSelectsAndSetPlaceholders() {
//     clearHTMLSelectChildrenFrom(issuerElement);
//     createSelectElementPlaceholder(issuerElement, issuerPlaceholder);
//
//     clearHTMLSelectChildrenFrom(installmentsElement);
//     createSelectElementPlaceholder(installmentsElement, installmentsPlaceholder);
// }
//
// function clearHTMLSelectChildrenFrom(element) {
//     element.innerHTML = '';
// }
//
// function createSelectElementPlaceholder(element, placeholder) {
//     const option = document.createElement('option');
//     option.textContent = placeholder;
//     option.selected = true;
//     option.disabled = true;
//     element.appendChild(option);
// }
//
// // Atualiza validações do cartão
// function updatePCIFieldsSettings(paymentMethod) {
//     const { settings } = paymentMethod;
//     const cardNumberSettings = settings[0].card_number;
//     const securityCodeSettings = settings[0].security_code;
//
//     cardNumberElement.update({ settings: cardNumberSettings });
//     securityCodeElement.update({ settings: securityCodeSettings });
// }
//
// async function updateIssuer(paymentMethod, bin) {
//     const { additional_info_needed, issuer } = paymentMethod;
//     let issuerOptions = [issuer];
//
//     if (additional_info_needed.includes('issuer_id')) {
//         issuerOptions = await getIssuers(paymentMethod, bin);
//     }
//
//     createSelectOptions(issuerElement, issuerOptions);
// }
//
// async function getIssuers(paymentMethod, bin) {
//     try {
//         const { id: paymentMethodId } = paymentMethod;
//         return await mp.getIssuers({ paymentMethodId, bin });
//     } catch (e) {
//         console.error('Erro ao obter emissores:', e);
//     }
// }
//
// async function updateInstallments(paymentMethod, bin) {
//     try {
//         const installments = await mp.getInstallments({
//             amount: document.getElementById('transactionAmount').value,
//             bin,
//             paymentTypeId: 'credit_card'
//         });
//
//         const installmentOptions = installments[0].payer_costs;
//         const installmentOptionsKeys = { label: 'recommended_message', value: 'installments' };
//         createSelectOptions(installmentsElement, installmentOptions, installmentOptionsKeys);
//     } catch (e) {
//         console.error('Erro ao obter parcelas:', e);
//     }
// }
//
// // ==========================
// // Criação do token do cartão
// // ==========================
// const formElement = document.getElementById('form-checkout');
// formElement.addEventListener('submit', createCardToken);
//
// async function createCardToken(event) {
//     try {
//         const tokenElement = document.getElementById('token');
//         if (!tokenElement.value) {
//             event.preventDefault();
//
//             const token = await mp.fields.createCardToken({
//                 cardholderName: document.getElementById('form-checkout__cardholderName').value,
//                 identificationType: document.getElementById('form-checkout__identificationType').value,
//                 identificationNumber: document.getElementById('form-checkout__identificationNumber').value,
//             });
//
//             tokenElement.value = token.id;
//             formElement.requestSubmit();
//         }
//     } catch (e) {
//         console.error('Erro ao criar token do cartão:', e);
//     }
// }
