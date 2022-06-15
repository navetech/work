// Set on load page callback
document.addEventListener("DOMContentLoaded", function() {
    const elem = document.querySelector("form");
    const selectedTargetLanguagesCountMax = elem.getAttribute("data-selected-target-languages-count-max");

    let selectedTargetLanguages = [];
    let selectedTargetLanguagesCount = 0;
    const nodeList = document.querySelectorAll(".select-target-language");
    for (let i = 0; i < nodeList.length; i++) {
        nodeList[i].checked = false;
        nodeList[i].value = nodeList[i].name;

        nodeList[i].onchange = (e) => {
            if (! e.target.checked ) {
                selectedTargetLanguagesCount--;
                ret = unselectTargetLanguage(e.target, selectedTargetLanguages);
                selectedTargetLanguages = ret["selectedTargetLanguages"]; 
                e.target.value = ret["value"];
            }
            else {
                if (selectedTargetLanguagesCount < selectedTargetLanguagesCountMax) {
                    selectedTargetLanguagesCount++;
                    ret = selectTargetLanguage(e.target, selectedTargetLanguages);
                    selectedTargetLanguages = ret["selectedTargetLanguages"]; 
                    e.target.value = ret["value"];
                }
                else {
                    e.target.checked = false;
                }
            } 

            showSelectedTargetLanguages(selectedTargetLanguages)
        };
    }
        
    showSelectedTargetLanguages(selectedTargetLanguages)
});


function unselectTargetLanguage(targetElem, selectedTargetLanguages) {
    const ret = {};

    const value = targetElem.name;
    ret["value"] = value;

    for (let i = 0; i < selectedTargetLanguages.length; i++) {
        if (selectedTargetLanguages[i].id == targetElem.id) {
            selectedTargetLanguages.splice(i, 1);
        }
    }

    const elem = document.querySelector("form");
    const languageToSortNumberSeparator = elem.getAttribute("data-language-to-sort-number-separator");

    for (let i = 0; i < selectedTargetLanguages.length; i++) {
        const value = selectedTargetLanguages[i].name + languageToSortNumberSeparator + i;
        selectedTargetLanguages[i].value = value;
    }

    ret["selectedTargetLanguages"] = selectedTargetLanguages; 

    return ret;
}


function selectTargetLanguage(targetElem, selectedTargetLanguages) {
    const ret = {};

    const elem = document.querySelector("form");
    const languageToSortNumberSeparator = elem.getAttribute("data-language-to-sort-number-separator");

    const value = targetElem.name + languageToSortNumberSeparator + selectedTargetLanguages.length;
    ret["value"] = value;

    selectedTargetLanguages.push(targetElem);

    ret["selectedTargetLanguages"] = selectedTargetLanguages; 

    return ret;
}


function showSelectedTargetLanguages(selectedTargetLanguages) {
    const label_elem = document.querySelector("#selected-target-languages-label"); 
    if (selectedTargetLanguages.length < 1) {
        label_elem.style.visibility = 'hidden';
    }
    else {
        label_elem.style.visibility = 'visible';
    }

    for (let i = 0; i < selectedTargetLanguages.length; i++) {
        selector = "#selected-target-language" + i
        const elem = document.querySelector(selector);

        elem.style.visibility = 'visible';

        labels = selectedTargetLanguages[i].labels
        elem.textContent = labels[0].textContent
    }

    const elem = document.querySelector("form");
    const selectedTargetLanguagesCountMax = elem.getAttribute("data-selected-target-languages-count-max");
    for (let i = selectedTargetLanguages.length; i < selectedTargetLanguagesCountMax; i++) {
        selector = "#selected-target-language" + i
        const elem = document.querySelector(selector);

        elem.style.visibility = 'hidden';
        elem.textContent = ''
    }
}
