// Set on load page callback
document.addEventListener("DOMContentLoaded", function() {
    const elem = document.querySelector("form");
    const selectedTargetLanguagesCountMax = elem.getAttribute("data-selected-target-languages-count-max");

    let selectedTargetLanguages = [];
    let selectedTargetLanguagesCount = 0;
    const nodeList = document.querySelectorAll(".select-target-language");
    for (let i = 0; i < nodeList.length; i++) {
        nodeList[i].checked = false;
        nodeList[i].value = nodeList[i].id;
        
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
                    e.target.checked = false
                    ret = unselectTargetLanguage(e.target, selectedTargetLanguages);
                    selectedTargetLanguages = ret["selectedTargetLanguages"]; 
                    e.target.value = ret["value"];
                    }
            } 
            console.log(e.target.checked);
        };
    }

    showSelectedTargetLanguages(selectedTargetLanguages)
});


function unselectTargetLanguage(elem, selectedTargetLanguages) {
    const ret = {}

    value = elem.id
    ret["value"] = value

    return ret
}
